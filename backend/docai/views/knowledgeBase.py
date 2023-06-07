from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from docai.models import Knowledge
from rest_framework.decorators import action
from django.conf import settings
import os

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
        return Response(serializer.data)
    
    # 重写删除，删除media中的文件
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        path = os.path.join(settings.MEDIA_ROOT, str(instance.file))
        os.remove(path)
        self.perform_destroy(instance)
        return Response({"code": 200, "msg": "删除成功"})











