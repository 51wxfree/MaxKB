# coding=utf-8
"""
    @project: maxkb
    @Author：虎
    @file： base_vector.py
    @date：2023/10/18 19:16
    @desc:
"""
from abc import ABC, abstractmethod
from typing import List, Dict

from langchain.embeddings import HuggingFaceEmbeddings

from common.config.embedding_config import EmbeddingModel
from embedding.models import SourceType


class BaseVectorStore(ABC):
    vector_exists = False

    @abstractmethod
    def vector_is_create(self) -> bool:
        """
        判断向量库是否创建
        :return: 是否创建向量库
        """
        pass

    @abstractmethod
    def vector_create(self):
        """
        创建 向量库
        :return:
        """
        pass

    def save_pre_handler(self):
        """
        插入前置处理器 主要是判断向量库是否创建
        :return: True
        """
        if not BaseVectorStore.vector_exists:
            if not self.vector_is_create():
                self.vector_create()
                BaseVectorStore.vector_exists = True
        return True

    def save(self, text, source_type: SourceType, dataset_id: str, document_id: str, paragraph_id: str, source_id: str,
             is_active: bool,
             embedding=None):
        """
        插入向量数据
        :param source_id:  资源id
        :param dataset_id: 数据集id
        :param text: 文本
        :param source_type: 资源类型
        :param document_id: 文档id
        :param is_active:   是否禁用
        :param embedding:   向量化处理器
        :param paragraph_id 段落id
        :return:  bool
        """
        if embedding is None:
            embedding = EmbeddingModel.get_embedding_model()
        self.save_pre_handler()
        self._save(text, source_type, dataset_id, document_id, paragraph_id, source_id, is_active, embedding)

    def batch_save(self, data_list: List[Dict], embedding=None):
        """
        批量插入
        :param data_list: 数据列表
        :param embedding: 向量化处理器
        :return: bool
        """
        if embedding is None:
            embedding = EmbeddingModel.get_embedding_model()
        self.save_pre_handler()
        self._batch_save(data_list, embedding)
        return True

    @abstractmethod
    def _save(self, text, source_type: SourceType, dataset_id: str, document_id: str, paragraph_id: str, source_id: str,
              is_active: bool,
              embedding: HuggingFaceEmbeddings):
        pass

    @abstractmethod
    def _batch_save(self, text_list: List[Dict], embedding: HuggingFaceEmbeddings):
        pass

    @abstractmethod
    def search(self, query_text, dataset_id_list: list[str], is_active: bool, embedding: HuggingFaceEmbeddings):
        pass

    @abstractmethod
    def update_by_paragraph_id(self, paragraph_id: str, instance: Dict):
        pass

    @abstractmethod
    def update_by_source_id(self, source_id: str, instance: Dict):
        pass

    @abstractmethod
    def delete_by_dataset_id(self, dataset_id: str):
        pass

    @abstractmethod
    def delete_by_document_id(self, document_id: str):
        pass

    @abstractmethod
    def delete_by_source_id(self, source_id: str, source_type: str):
        pass

    @abstractmethod
    def delete_by_paragraph_id(self, paragraph_id: str):
        pass
