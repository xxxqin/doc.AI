from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from docai.models import Page, Block
from rest_framework.decorators import action
from django.conf import settings
import os
from docai.views.textAIUtills import translate, summary, continueText, emailText, proofread, qa_ai,meetingText





### 序列化器 ###

class BlockSerializer(ModelSerializer):
    """ 块序列化器 """

    class Meta:
        model = Block
        fields = "__all__"



### 视图集 ###



# 新增块，新增后，将块的id加入到page的block_seq中，且在block_id后面
def insert_block_after(block_id, text):
    block = Block.objects.get(id=block_id)
    page = block.page
    new_block = Block.objects.create(
        type="text",
        data={"text": text},
        page=page
    )

    page.block_seq.insert(page.block_seq.index(block_id) + 1, new_block.id)
    page.save()
    return None


class BlockViewSet(ModelViewSet):
    """ 块视图集 """
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    # AI问答
    # url: /api/docai/block_ai/qa/
    # method: post
    @action(methods=['post'], detail=False)
    def qa(self, request):
        block_id = request.data.get("block_id")
        content = request.data.get("content")
        block = Block.objects.get(id=block_id)
        if not block:
            return Response({"code": 400, "msg": "数据不存在"})
        
        ai_data = qa_ai(content)
        if ai_data.get("success"):
            text = ai_data.get("text")
            block.data["text"] = text
            block.save()


        return Response({"code": 200, "msg": "success"})



    
    # 块级AI操作
    # url: /api/docai/block_ai/{pk}/handle_ai/
    # method: post
    @action(methods=['post'], detail=True)
    def handle_ai(self, request, pk=None):
        type = request.data.get("type")
        block_id = int(pk)

        block = Block.objects.get(id=block_id)
        if not block:
            return Response({"code": 400, "msg": "数据不存在"})
       
        web_text = block.data.get("text")
        if type == "trans":
            trans_type = request.data.get("trans_type")
            ai_data = translate(web_text, trans_type)
            if ai_data.get("success"):
                text = ai_data.get("text")
                insert_block_after(block_id, text)

        if type == "summary":
            ai_data = summary(web_text)
            if ai_data.get("success"):
                text = ai_data.get("text")
                #新增块，新增后，将块的id加入到page的block_seq中，且在block_id后面
                insert_block_after(block_id, text)

        if type == "continue":
            ai_data = continueText(web_text)
            if ai_data.get("success"):
                text = ai_data.get("text")

                #新增块，新增后，将块的id加入到page的block_seq中，且在block_id后面
                insert_block_after(block_id, text)
        
        if type == "email":
            ai_data = emailText(web_text)
            if ai_data.get("success"):
                text = ai_data.get("text")

                #新增块，新增后，将块的id加入到page的block_seq中，且在block_id后面
                insert_block_after(block_id, text)

        if type == "proofread":
            ai_data = proofread(web_text)
            if ai_data.get("success"):
                text = ai_data.get("text")

                insert_block_after(block_id, text)

        if type == "meeting":
            ai_data = meetingText(web_text)
            if ai_data.get("success"):
                text = ai_data.get("text")

                insert_block_after(block_id, text)


        return Response({"code": 400, "msg":ai_data})





    






