#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@Project: EasyLLM
@File   : base.py
@Version: V1.0.0
@Author : WenC
@Time   : 2025-12-02 23:22:37
@Email  : mr.wenc2640@gmail.com
@License: (C)Copyright 2020-2030,Mr.WenC
@Desc   :
"""

# here put the import lib

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from langchain_core.documents import Document


class BaseVectorStore(ABC):
    """
    向量数据库存储基类，定义了所有向量数据库存储必须遵循的接口
    遵循依赖倒置原则，允许后续使用不同的向量数据库
    """

    @abstractmethod
    def add(self, documents: List[Document]) -> List[str]:
        """
        添加文档到向量库存储

        :param documents: 要添加的文档列表
        :return: 文档ID列表
        """
        pass

    @abstractmethod
    def search(
            self, query: str, k: int = 5, condition: Optional[Dict] = None) -> List[Document]:
        """
        基于查询字符串检索相关文档
        :param query: 查询的字符串
        :param k: 返回的最大文档数量
        :param condition: 过滤条件，可用于metadata过滤，
        :return: 相关文档列表
        """
        pass

    @abstractmethod
    def delete(self, documents: List[str]) -> bool:
        """
        删除指定ID的文档
        :param documents: 需要删除的文档ID列表
        :return: 是否删除成功
        """
        pass

    @abstractmethod
    def as_retriever(self, **kwargs) -> Any:
        """
        返回一个检索器对象，用于RAG链中使用
        :param kwargs: 检索器的配置参数
        :return: 检索器对象
        """

    @abstractmethod
    def close(self) -> None:
        """
        关闭向量数据库连接
        :return:
        """
        pass
