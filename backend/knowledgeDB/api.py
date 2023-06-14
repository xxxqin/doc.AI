import os
import re
import pickle
from pathlib import Path
from chardet.universaldetector import UniversalDetector
from llama_index.readers import SimpleDirectoryReader
from llama_index import load_index_from_storage, StorageContext, GPTTreeIndex, GPTVectorStoreIndex, \
    GPTKeywordTableIndex, GPTRAKEKeywordTableIndex, GPTListIndex

from typing import Dict, Type

from llama_index.readers.base import BaseReader
from llama_index.readers.file.docs_reader import DocxReader, PDFReader
from llama_index.readers.file.epub_reader import EpubReader
from llama_index.readers.file.image_reader import ImageReader
from llama_index.readers.file.ipynb_reader import IPYNBReader
from llama_index.readers.file.markdown_reader import MarkdownReader
from llama_index.readers.file.mbox_reader import MboxReader
from llama_index.readers.file.slides_reader import PptxReader
from llama_index.readers.file.tabular_reader import PandasCSVReader
from llama_index.readers.file.video_audio_reader import VideoAudioReader
from llama_index.readers.schema.base import Document

DEFAULT_FILE_READER_CLS: Dict[str, Type[BaseReader]] = {
    ".pdf": PDFReader,
    ".docx": DocxReader,
    ".pptx": PptxReader,
    ".jpg": ImageReader,
    ".png": ImageReader,
    ".jpeg": ImageReader,
    ".mp3": VideoAudioReader,
    ".mp4": VideoAudioReader,
    ".csv": PandasCSVReader,
    ".epub": EpubReader,
    ".md": MarkdownReader,
    ".mbox": MboxReader,
    ".ipynb": IPYNBReader,
}

DEFAULT_STORE_MODE = {'GPTVectorStoreIndex': GPTVectorStoreIndex,
                      'GPTListIndex': GPTListIndex,
                      'GPTTreeIndex': GPTTreeIndex,
                      'GPTKeywordTableIndex': GPTKeywordTableIndex,
                      'GPTRAKEKeywordTableIndex': GPTRAKEKeywordTableIndex}


class AI_knowledge:
    def __init__(self, knowledge_base_path, save_path='./example/storage', index_type='GPTListIndex'):
        self.INDEX_METHOD = DEFAULT_STORE_MODE[index_type]
        self.save_path = save_path
        if self.load(save_path):
            print('Load index from {}'.format(save_path))
        else:
            self.read_local_data(knowledge_base_path)
        self.query_engine = self.index.as_query_engine()
        self.supported_suffix = list(DEFAULT_FILE_READER_CLS.keys())
        self.file_extractor = {}

    def save(self, save_path=None):
        if save_path is None:
            save_path = self.save_path
        self.index.storage_context.persist(persist_dir=save_path)

    def load(self, load_path=None):
        # 先判断文件是否存在，不存在则返回False
        if load_path is None:
            load_path = self.save_path
        if not os.path.exists(load_path):
            print('文件不存在')
            return False
        print('文件存在，开始加载')
        storage_context = StorageContext.from_defaults(persist_dir=load_path)
        index = load_index_from_storage(storage_context)
        if type(index) == self.INDEX_METHOD:
            self.index = index
            return True
        else:
            raise TypeError(f'知识库类型不匹配，所加载知识库类型为{type(index)}，而所需知识库类型为{self.INDEX_METHOD}\n请修改参数重新加载，或者删除{load_path}文件夹重新加载')

    def query(self, question):
        response = self.query_engine.query(question)
        return response.response

    def get_files_list(self):
        # 返回已加载入知识库的文件列表
        file_set = set()
        for file_info in list(self.index.ref_doc_info.keys()):
            file = re.sub(r'_part_\d+', '', file_info)
            file_set.add(file)
        return list(file_set)

    def query_with_select_file(self, question, file_paths):
        # 限定查询范围为file_names中的文件
        index = self.INDEX_METHOD([])
        file_names = [Path(file_path).name for file_path in file_paths]
        for file_info in list(self.index.ref_doc_info.keys()):
            file = re.sub(r'_part_\d+', '', file_info)
            if Path(file).name in file_names:
                doc_ids = self.index.ref_doc_info[file_info].doc_ids
                nodes = [self.index.docstore.docs[doc_id] for doc_id in doc_ids]
                for node in nodes:
                    index.insert(node)
        query_engine = index.as_query_engine()
        response = query_engine.query(question)
        return response.response

    def insert(self, file_path):

        file_path = Path(file_path)
        file_suffix = file_path.suffix.lower()
        if file_suffix in self.supported_suffix:
            # use file readers
            if file_suffix not in self.file_extractor:
                # instantiate file reader if not already
                reader_cls = DEFAULT_FILE_READER_CLS[file_suffix]
                self.file_extractor[file_suffix] = reader_cls()
            reader = self.file_extractor[file_suffix]
            docs = reader.load_data(file_path)

            # iterate over docs
            for i, doc in enumerate(docs):
                doc.doc_id = f"{str(file_path)}_part_{i}"

            for doc in docs:
                self.index.insert(doc)

        else:
            # do standard read
            with open(file_path, "r", errors='ignore', encoding=self.detect_encoding(file_path)) as f:
                data = f.read()

            doc = Document(data)
            doc.doc_id = str(file_path)

            self.index.insert(doc)

    def delete(self, file_name):
        wait_delete = []
        file_name = Path(file_name).name
        for file_info in self.index.ref_doc_info.keys():
            file = re.sub(r'_part_\d+', '', file_info)
            if file_name == Path(file).name:
                wait_delete.append(file_info)

        for doc_id in wait_delete:
            #self.index.delete(doc_id)
            self.index.delete_ref_doc(doc_id)

        # True if delete successfully
        return True if len(wait_delete) > 0 else False

    # 其实就是先删除再插入
    def update(self, file_path):
        self.delete(file_path)
        self.insert(file_path)

    # 检测文件编码格式的
    def detect_encoding(self, file_path):
        detector = UniversalDetector()
        for line in open(file_path, 'rb'):
            detector.feed(line)
            if detector.done: break
        detector.close()
        return detector.result['encoding']

    def read_local_data(self, knowledge_base_path, auto_save=True):
        documents = SimpleDirectoryReader(knowledge_base_path, errors='ignore', filename_as_id=True).load_data()
        self.index = self.INDEX_METHOD.from_documents(documents)
        if auto_save:
            self.save()
