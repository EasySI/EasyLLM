# 笔记4

# 内容总结

Decoder一章主要讲解了Decoder的解码流程、结构，重点讲解了掩码（Mask）机制，包括填充掩码和因果掩码（屏蔽未来信息）。本章还讲解了Decoder在不同阶段的信息传递机制，以及模型的评估和训练。最后，本章总结了Transformer之后的高级主题和应用。
Tokenization一章则主要说明现在的主流分词方法，尤其是中文字符的分词方法。





## 什么时候 Encoder 才会与 Decoder 进行 Cross-Attention？/ Encoder 是怎么堆叠的？

```rust
输入序列  --->  Embedding + 位置编码  --->  Encoder Layer 1
                                                    ↓
                                                Encoder Layer 2
                                                    ↓
                                                Encoder Layer 3
                                                    ↓
                                                    ...
                                                    ↓
                                                Encoder Layer N
                                                    ↓
                                           最终 Encoder 输出 (Memory)
```
输入序列经过 N 层 Encoder 处理后，最终的输出（称为 Memory）将被传递给 Decoder 的 Cross-Attention。Decoder 只在 Cross-Attention 计算时需要 Encoder 的输出，即在每个 Decoder Layer 中。
- Encoder 的每一层都不会与 Decoder 交互，只有**完整的** Encoder 计算完成后（即 N 层全部计算完）才会与 Decoder 交互。
- Decoder 的 Cross-Attention 只使用 Encoder 最后一层的输出（Memory），即Cross Attention(Q = Decoder, K,V = Encoder's Final output )



## 总结Transformer中的注意力运算

假设X是编码器的输入，Y是解码器的当前输入（此前的输出），H是编码器的最终输出。

|注意力类型|Query（Q）|Key（K）|Value（V）|作用|
|-----|------|-----|-----|-----|
|自注意力（Encoder Self-Attention）|X变换|X变换|X变换|让每个 token 关注**整个输入序列**| 
|自注意力（Decoder Self-Attention）|Y变换|Y变换|Y变换|让解码器关注**已生成的 token**（Mask 未来 token）| 
|交叉注意力（Decoder Cross-Attention）|Y变换|H变换|H变换|让解码器关注**编码器的输出**| 

![注意力运算](images/Attention1.png)








## 补充：自回归（Autoregressive）和非自回归（Non-Autoregressive）

自回归任务（Autoregressive, AR） 指的是当前时间步的输出**依赖于之前时间步**的输出，并且模型在推理时**按顺序**生成数据，每一步都基于已经生成的部分。

在自回归模型中，下一个 token（或数据点）是根据之前已生成的 token 预测的，而不是同时计算所有 token。

||自回归|非自回归|
|----|----|----|
|特点|逐步生成token，每一步依赖前一步|一次性生成所有token|
|推理速度|**慢**（必须按顺序预测）|**快**可以并行预测|
|模型例子|GPT、Transformer解码器|BERT|
|应用|语音建模、机器翻译、语音合成|BERT预训练、图像分类|





# 问题解答



