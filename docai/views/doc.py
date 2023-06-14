from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from docai.models import Page, Block
from rest_framework.decorators import action
from django.conf import settings
import os

### 序列化器 ###

class BlockSerializer(ModelSerializer):
    """ 块序列化器 """

    class Meta:
        model = Block
        fields = "__all__"


class PageSerializer(ModelSerializer):
    """ 
    页面列化器 for detail 
    包括block信息
    """
    block_set = BlockSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = "__all__"

class PageListSerializer(ModelSerializer):
    """ 
    页面列化器, for list
    用于获取全部页面时使用 
    不包括block信息
    """

    class Meta:
        model = Page
        fields = "__all__"



### 视图集 ###
class PageViewSet(ModelViewSet):
    """ 页面视图集 """
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    # 重写新建方法，每次新建页面时，自动创建一个空文本块
    def create(self, request, *args, **kwargs):
        page = Page.objects.create()

        text = Block.objects.create(
            type="text",
            data={"text": ""},
            page=page
            )
        
        # 文本块的id加入到page的block_seq中
        page.block_seq.append(text.id)
        page.save()

        return Response({"code": 200, "msg": "新增成功"})

    # 重写获取全部，只返回page信息，不包括block信息
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PageListSerializer(queryset, many=True)
        return Response(serializer.data)



    
class BlockViewSet(ModelViewSet):
    """ 块视图集 """
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    # 重写删除，如果是image类型的块，删除块的同时，删除图片。以及删除块后，将块的id从page的block_seq中删除
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.type == "image":
            image_path = instance.data["text"]
            if os.path.exists(image_path):
                os.remove(image_path)
        page = instance.page
        page.block_seq.remove(instance.id)
        page.save()
        self.perform_destroy(instance)
        return Response({"code": 200, "msg": "删除成功"})
    
    # 重写新增，新增后，将块的id加入到page的block_seq中，且在指定id后面
    def create(self, request, *args, **kwargs):
        target_id = request.data["target_id"]
        page_id = request.data["page_id"]
        type = request.data["type"]
        data = request.data["data"]

        page = Page.objects.get(id=page_id)

        # 新建块
        block = Block.objects.create(
            type=type,
            data=data,
            page=page
            )
        
        # 将块的id加入到page的block_seq中
        page.block_seq.insert(page.block_seq.index(target_id) + 1, block.id)
        page.save()

        # 如果新建的是image类型的块，则判断新建的image块的id是否在block_seq的最后一位，若是则再新建一个空文本块
        if type == "image":
            if page.block_seq.index(block.id) == len(page.block_seq) - 1:
                text = Block.objects.create(
                    type="text",
                    data={"text": ""},
                    page=page
                    )
                page.block_seq.append(text.id)
                page.save()
        print({"id": block.id})
        return Response({"code": 200, "msg": "新增成功", "data": {"id": block.id}})
    

    # 给image块上传图像
    # url: /api/docai/block/add_image/
    @action(methods=["post"], detail=False)
    def add_image(self, request, *args, **kwargs):
        block_id = request.data["block_id"]
        image = request.FILES.get("pic")

        block = Block.objects.get(id=block_id)

        #判断图片大小小于4M,大于4M则返回错误
        if image.size > 4 * 1024 * 1024:
            return Response({"code": 400, "msg": "图片大小不能超过4M"})
        
        #判断图片类型是否为图片
        if image.content_type not in ["image/jpeg", "image/png", "image/gif"]:
            return Response({"code": 400, "msg": "图片类型错误"})
        
        #保存图片到media文件夹，地址为：media/note/page id/image/块id/图片名


        image_path = os.path.join(settings.MEDIA_ROOT, str('note'), str(block.page.id), str('image'), str(block.id), str(image.name))
        if not os.path.exists(os.path.dirname(image_path)):
            os.makedirs(os.path.dirname(image_path))

        with open(image_path, "wb") as f:
            for chunk in image.chunks():
                f.write(chunk)

        path = image_path.replace("\\", '/')

        #更新块数据
        block.data = {"text": path}
        block.save()
        return Response({"code": 200, "msg": "新增成功"})





