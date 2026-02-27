# Transformer
本课程涵盖了Transformer的核心组成部分，包含Transformer编码器和解码器的实现。
课程结合代码解读知识点，同时通过形象生动的例子，为学习者理解Transformer模型提供参考和借鉴。
实践项目无需依赖任何深度学习框架，完全从零开始，使用基础的Numpy等科学计算库实现Transformer，旨在深化学习者对模型本质的理解与掌握。
最后，使用Transformer模型实现在机器翻译任务中的应用，加深对模型的理解


## 课程大纲
| 章节  | 内容 | 代码实现|
| ------------- | ------------- |------------- |
| 第一章 | 引言|词嵌入（低维映射到高维）|
| 第二章 | Transformer简述 |  相对位置向量, WordVec |
| 第三章 | Encoder结构（Encoder）| 交叉注意力（Cross-Attention） |
| 第四章 | Decoder结构（Decoder）| bert（apply-bert）、gpt（apply-gpt） |
| 第五章 | 项目实践 | 机器翻译项目案例、Transformer结构拆解、使用 NumPy 和 SciPy 实现通用注意力机制|

## 目录
第一章 引言
- 1. 序列到序列（Seq2Seq）模型概述
- 2. Encoder-Decoder模型概述
- 3. Attention 的提出与影响

第二章 Transformer简述
- 1. Attention 机制
- 2. Transformer概述
- 3. Transformer vs CNN vs RNN
- 4. 输入嵌入(Input Embedding)
- 5. Multi-Head Attention vs Multi-Head Self-Attention
- 6. 词向量生成过程

第三章 Encoder结构
-  1. 编码器(Encoder)
- 2. 多头自注意力(Multi-Head Self-Attention)
- 3. 交叉自注意力(Cross Attention)
- 4. Cross Attention 和 Self Attention 主要的区别

第四章 Decoder结构
- 1. 解码器(Decoder)
- 2. 掩码(Mask)
- 3. 模型的训练与评估
- 4. 高级主题和应用
- 5. Tokenization
  
第五章 Project
- 1. 项目案例
- 2. 使用NumPy和SciPy实现通用注意力机制
- 3. 一键运行Transformer板块（Transformer组件实现）
- 4. Multi-head attention（多头注意力机制）
- 5. Self attention（自注意力机制实现）
