# 一个知识库的API
## 介绍
这是一个知识库的API，可以将知识库中的文本进行索引，然后通过用户的问题，查询出答案。
加载该API的方法如下：
```python
from api import AI_knowledge
```
具体的方法请阁下移步示例代码[example](./example.ipynb)

## 调用前的准备
你需要将代理地址和openai key写入环境变量中，或者直接在代码中写入，如下所示：
```python
import os

os.environ["HTTP_PROXY"] = "http://127.0.0.1:10809"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:10809"
os.environ["OPENAI_API_KEY"] = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

## 初始化知识库
知识库是个文件夹，你需要将所需的文件（word文档，txt文档，excel表格等）塞入此处，如下面的`./example/knowledge-base`就是一个知识库
这一步一定要网络好，不然半天都不会出结果的。

```python
from api import AI_knowledge
engine = AI_knowledge(knowledge_base_path='./example/knowledge-base', save_path='./example/storage', index_type='GPTTreeIndex')
```

## 接口说明
- `def __init__(self, knowledge_base_path, save_path='./example/storage'', index_type='GPTListIndex')`
    - knowledge_base_path: 知识库的路径，是个文件夹，里面的文件就是知识。支持多种格式，建议放入格式有：
        - `.pdf`
        - `.docx`
        - `.pptx`
        - `.md`
        - `.ipynb`
        - 为打开上述格式的文件，需要安装对应的库，如
          - `.docx`和`.pdf`需要安装`pip install docx2txt`, 
          - `.pptx`需要安装`pip install python-pptx`, 
          - `.ipynb`需要安装`pip install nbconvert`
            ```python
            pip install docx2txt
            pip install torch transformers python-pptx Pillow
            pip install nbconvert
            ```
    - save_path: 索引文件的保存路径，保存后可以直接加载索引，不用再次建立索引。
    - index_type: 索引类型，目前支持五种：
        - `GPTVectorStoreIndex`: 将文本切成多段，然后进行Embedding。在query时，将查询文本也进行Embedding，然后计算相似度，查找出最相似的文本片段，再将文本片段传入LLM进行问答。又快又高效。
        - `GPTListIndex`: 将文本切成多段，查询时按照顺序逐个进行query操作。每一次答案都会对前一个答案进行refine操作。
        - `GPTTreeIndex`：将文本切成多段，然后总结每段的内容。到了用户query阶段，将这些的总结发给LLM，让LLM选择其中的几个节点，然后对选中的节点进行query。
        - `GPTKeywordTableIndex`：将文本切成多段，让LLM提取每段的关键词。到了用户query阶段，提取用户query的关键词，通过关键词搜索最相关的文本片段，再将文本片段传入LLM进行问答。
        - `GPTRAKEKeywordTableIndex`：我忘记是啥了。


- `def save(self, save_path=None)`
  - 保存索引文件，保存后可以直接加载索引，不用再次建立索引。
    - save_path: 索引文件的保存路径，保存后可以直接加载索引，不用再次建立索引。如果不指定，则使用初始化时的save_path。

- `def load(self, load_path=None)`
  - 加载索引文件，加载后可以直接使用索引。
    - load_path: 索引文件的保存路径，保存后可以直接加载索引，不用再次建立索引。如果不指定，则使用初始化时的save_path。

- `def query(self, question)`
  - 查询，返回答案，类型为`str`。
    - question: 用户的问题，字符串类型。

- `def get_files_list(self)`
  - 返回知识库中的文件列表，类型为`list`，包含了文件的路径和文件的名称。

- `def query_with_select_file(self, question, file_paths)`
  - 选择性的查询，只在指定的文件中查询。
    - question: 用户的问题，字符串类型。
    - file_paths: 文件名列表，类型为`list`。

- `def insert(self, file_path)`
  - 插入新的文件，是单个文件
    - file_path: 文件路径

- `def delete(self, file_name)`
  - 删除文件，只是在索引中删除，不会在硬盘上删除文件
    - file_name: 文件名

- `def update(self, file_path)`
  - 更新文件，是单个文件（其实就是先删除再插入）
    - file_path: 文件路径

- `def read_local_data(self, knowledge_base_path, auto_save=True)`
  - 读取本地数据，建立索引，在初始化时已经调用了，一般不需要再调用。
    - knowledge_base_path: 知识库的路径，是个文件夹，里面的文件就是知识，支持多种格式。
    - auto_save: 是否自动保存索引文件，默认为True