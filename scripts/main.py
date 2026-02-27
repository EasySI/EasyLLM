#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File   : main.py
@Version: V1.0.0
@Author : WenC
@Time   : 2025-12-02 21:57:24
@Email  : mr.wenc2640@gmail.com
@License: (C)Copyright 2020-2030,Mr.WenC
@Desc   :
"""

# here put the import lib
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

docs = TextLoader("./data.txt", encoding="utf-8").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10).split_documents(
    docs)

vectorstore = Chroma.from_documents(chunks, OllamaEmbeddings(model="qwen3:8b"))


@tool
def search(query: str) -> str:
    """从知识库中检索与问题相关的文本片段。"""
    documents = vectorstore.similarity_search(query=query, k=4)
    for doc in documents:
        print(doc.page_content)
        print("=====================" * 20)
    return "\n\n".join([doc.page_content for doc in documents])


llm = ChatOllama(model="qwen3:8b")
agent = create_agent(model=llm, tools=[search],
                     system_prompt="你是一个智能助手，你可以从知识库中检索与问题相关的文本片段。")

if __name__ == '__main__':
    for resp in agent.stream({"messages": [{"role": "user", "content": "七十二变"}]}):
        print(resp)
