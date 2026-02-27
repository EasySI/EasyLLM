#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File   : main.py
@Version: v1.0.0
@Author : WenC
@Time   : 2025-11-24 09:49:12
@Email  : mr.wenc2640@gmail.com
@License: (C)Copyright 2025-2035, WenC
@Desc   : 
"""

# here put the import lib

# from langchain_ollama import ChatOllama
# from langchain.agents import create_agent
# from langchain_community.tools.tavily_search import TavilySearchResults
#
# model = ChatOllama(model="qwen3:8b")
#
# web_search = TavilySearchResults(max_results=2)
#
# agent = create_agent(
#     model=model,
#     tools=[web_search],
#     system_prompt="你是一名多才多艺的智能助手，可以调用工具帮助用户解决问题。"
# )
#
# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "请帮我查询2024年诺贝尔物理学奖得主是谁？"}]}
# )
#
# print(result['messages'][-1].content)


# import torch
# from vllm import LLM
#
#
# def get_detailed_instruct(task_description: str, query: str) -> str:
#     return f"Instruct: {task_description}\nQuery: {query}"
#
#
# task = "Given a web search query, retrieve relevant passages that answer the query."
# queries = [
#     get_detailed_instruct(task, "What is the capital of China?"),
#     get_detailed_instruct(task, "Explain gravity")
# ]
#
# documents = [
#     "The capital of China is Beijing",
#     "Gravity is a force that attracts two bodies towards each other. It gives weight to physical objects and is responsible for the movement of planets around the sun."
# ]
#
# input_texts = queries + documents
# model = LLM(model="./models/Qwen/Qwen3-Embedding-0.6B", task="embed")
#
# outputs = model.embed(input_texts)
# embeddings = torch.tensor([out.outputs.embedding for out in outputs])
#
# scores = (embeddings[:2] @ embeddings[2:].T)
# print(scores.tolist())


import math
import torch
from vllm import LLM, SamplingParams
from vllm.inputs.data import TokensPrompt
from modelscope import AutoTokenizer, is_torch_npu_available
from vllm.distributed.parallel_state import destroy_model_parallel


def format_instruction(instruction, query, doc):
    text = [
        {"role": "system",
         "content": "Judge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be \"yes\" or \"no\"."},
        {"role": "user",
         "content": f"<Instruct>: {instruction}\n\n<Query>: {query}\n\n<Document>: {doc}"}
    ]
    return text


def process_inputs(pairs, instruction, max_length, suffix_tokens):
    messages = [format_instruction(instruction, query, doc) for query, doc in pairs]
    messages = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=False, enable_thinking=False
    )
    messages = [ele[:max_length] + suffix_tokens for ele in messages]
    messages = [TokensPrompt(prompt_token_ids=ele) for ele in messages]
    return messages


def compute_logits(model, messages, sampling_params, true_token, false_token):
    outputs = model.generate(messages, sampling_params, use_tqdm=False)
    scores = []
    for i in range(len(outputs)):
        final_logits = outputs[i].outputs[0].logprobs[-1]
        token_count = len(outputs[i].outputs[0].token_ids)
        if true_token not in final_logits:
            true_logit = -10
        else:
            true_logit = final_logits[true_token].logprob
        if false_token not in final_logits:
            false_logit = -10
        else:
            false_logit = final_logits[false_token].logprob
        true_score = math.exp(true_logit)
        false_score = math.exp(false_logit)
        score = true_score / (true_score + false_score)
        scores.append(score)
    return scores


number_of_gpu = torch.cuda.device_count()
tokenizer = AutoTokenizer.from_pretrained('./models/Qwen/Qwen3-Reranker-0.6B')
model = LLM(
    model='./models/Qwen/Qwen3-Reranker-0.6B', tensor_parallel_size=number_of_gpu,
    max_model_len=10000, enable_prefix_caching=True, gpu_memory_utilization=0.8)
tokenizer.padding_side = "left"
tokenizer.pad_token = tokenizer.eos_token
suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
max_length = 8192
suffix_tokens = tokenizer.encode(suffix, add_special_tokens=False)
true_token = tokenizer("yes", add_special_tokens=False).input_ids[0]
false_token = tokenizer("no", add_special_tokens=False).input_ids[0]
sampling_params = SamplingParams(
    temperature=0,
    max_tokens=1,
    logprobs=20,
    allowed_token_ids=[true_token, false_token],
)

task = 'Given a web search query, retrieve relevant passages that answer the query'
queries = [
    "What is the capital of China?",
    "Explain gravity",
]

documents = [
    "The capital of China is Beijing.",
    "Gravity is a force that attracts two bodies towards each other. It gives weight to physical objects and is responsible for the movement of planets around the sun.",
]

pairs = list(zip(queries, documents))
inputs = process_inputs(pairs, task, max_length - len(suffix_tokens), suffix_tokens)
scores = compute_logits(model, inputs, sampling_params, true_token, false_token)
print('scores', scores)

destroy_model_parallel()
