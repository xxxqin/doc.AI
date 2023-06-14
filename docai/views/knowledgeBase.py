from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from docai.models import Knowledge, Block
from rest_framework.decorators import action
from django.conf import settings
import os
from knowledgeDB.api import AI_knowledge





# 初始化知识库






### 序列化器 ###

class KnowledgeSerializer(ModelSerializer):
    """ 
    知识库列化器
    """
    class Meta:
        model = Knowledge
        fields = "__all__"



### 视图集 ###

class KnowledgeViewSet(ModelViewSet):
    """ 知识库视图集 """

    queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializer

    # 知识库相关
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:10809"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:10809"
    os.environ["OPENAI_API_KEY"] = "xxxx"
    engine = AI_knowledge(knowledge_base_path='./media/knowledgeDB', save_path='./knowledgeDB/example/storage', index_type='GPTTreeIndex')

    # 重写新建方法，从file中确定name和type,然后，一起新建
    def create(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        name = file.name
        type = name.split(".")[-1]
        name = name.split(".")[0]
        data = {
            "name": name,
            "type": type,
            "file": file
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.engine = AI_knowledge(knowledge_base_path='./media/knowledgeDB', save_path='./knowledgeDB/example/storage', index_type='GPTTreeIndex')
        return Response(serializer.data)
    
    # 重写删除，删除media中的文件
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        path = os.path.join(settings.MEDIA_ROOT, str(instance.file))
        os.remove(path)
        self.perform_destroy(instance)
        return Response({"code": 200, "msg": "删除成功"})
    


    # 问答
    # url: /api/docai/knowledge/qa/
    # method: post
    @action(methods=['post'], detail=False)
    def qa(self, request):
        print("answer")
        content = request.data.get("content")
        block_id = request.data.get("block_id")
        answer = self.engine.query(content)
        print(answer)
        if not answer:
            return Response({"code": 400, "msg": "查询失败", "type":"bad"})
        else:
        # 新增块，新增后，将块的id加入到page的block_seq中，且在block_id后面
            block = Block.objects.get(id=block_id)
            page = block.page
            new_block = Block.objects.create(
                type="text",
                data={"text": answer},
                page=page
            )

            page.block_seq.insert(page.block_seq.index(block_id) + 1, new_block.id)
            page.save()

        return Response({"code": 200, "msg": "查询成功", "data": answer})











