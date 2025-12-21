#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@Project: EasyLLM
@File   : chroma_vector_store.py
@Version: V1.0.0
@Author : WenC
@Time   : 2025-12-02 23:42:48
@Email  : mr.wenc2640@gmail.com
@License: (C)Copyright 2020-2030,Mr.WenC
@Desc   :
"""

# here put the import lib
import os
from typing import Any, Optional, List, Dict
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from .base import BaseVectorStore


class ChromaVectorStore(BaseVectorStore):
    """
    Chroma向量数据库
    """

    def __init__(
            self, embedding: Any,
            persist_directory: Optional[str] = None,
            collection_name: str = "default"
    ):
        """
        初始化Chroma向量存储
        :param embedding: 嵌入模型
        :param persist_directory: 持久化目录路径
        :param collection_name: 集合名称
        """
        self.embedding = embedding
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self._store = Chroma(
            collection_name=collection_name,
            embedding_function=embedding,
            persist_directory=persist_directory
        )

    def add(self, documents: List[Document]) -> List[str]:
        """添加文档到Chroma向量数据库"""
        for doc in documents:
            if "source" not in doc.metadata and hasattr(doc, "metadata"):
                doc.metadata["source"] = "unknown"
        return self._store.add_documents(documents=documents)

    def search(
            self, query: str, k: int = 5, condition: Optional[Dict] = None) -> List[Document]:
        """在Chroma中检索相关文档，支持基于metadata过滤"""
        if condition:
            return self._store.similarity_search(query=query, k=k, filter=condition)
        else:
            return self._store.similarity_search(query=query, k=k)

    def delete(self, documents: List[str]) -> bool:
        """从Chroma中删除文档"""
        try:
            self._store.delete(ids=documents)
            return True
        except Exception as ex:
            raise Exception(f"Delete document error: {ex}")

    def as_retriever(self, **kwargs) -> Any:
        """返回Chroma检索器，支持过滤参数"""
        filter_params = kwargs.pop("filter", None)
        if filter_params:
            retriever = self._store.as_retriever(**kwargs)
            # 包装检索器以应用过滤器
            original_get_relevant_documents = retriever.get_relevant_documents

            def wrapped_get_relevant_documents(query, **retriever_kwargs):
                # 合并过滤条件
                combined_filter = {**filter_params, **retriever_kwargs.get("filter", {})}
                return original_get_relevant_documents(query, filter=combined_filter)

            retriever.get_relevant_documents = wrapped_get_relevant_documents
            return retriever
        else:
            return self._store.as_retriever(**kwargs)

    def close(self) -> None:
        pass

    def get_existing_documents(self) -> List[str]:
        """
        获取向量数据库中所有文档的source信息
        :return: 包含所有文档source的列表，同时包含原始路径和规范路径
        """
        try:
            results = self._store.get()
            if 'metadata' in results and results["metadata"]:
                sources = []
                for metadata in results["metadata"]:
                    if isinstance(metadata, dict):
                        source = metadata.get("source") or metadata.get('file_path')
                        if source:
                            sources.append(source)
                            # 添加规范化路径（处理路径分隔符差异和绝对/相对路径）
                            try:
                                # 尝试获取绝对路径
                                abs_path = os.path.abspath(source)
                                if abs_path not in sources:
                                    sources.append(abs_path)
                                # 尝试获取文件名（仅文件名匹配）
                                filename = os.path.basename(source)
                                if filename not in sources:
                                    sources.append(filename)
                            except:
                                # 如果规范化失败，忽略
                                pass
                return sources
            return []
        except Exception as ex:
            import traceback
            traceback.print_exc()
            raise Exception(f"获取现有文档信息时出错: {str(ex)}")

    def count(self)->int:
        """
        获取向量数据库中文档数量
        :return: 文档数量
        """
        try:
            results = self._store.get()
            if "ids" in results:
                return len(results["ids"])
            return 0
        except Exception as ex:
            raise Exception(f"获取文档数量时出错: {str(ex)}")