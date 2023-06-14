from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from docai.models import Page, Block
from django.conf import settings
import os
import json
import time
import requests
from docai.views.textAIUtills import translate

### 序列化器 ###

class BlockSerializer(ModelSerializer):
    """ 块序列化器 """

    class Meta:
        model = Block
        fields = "__all__"


### 视图集 ###


class ImageGenView(APIView):

    def post(self, request):
        block_id = request.data.get("block_id")
        content = request.data.get("content")

        block = Block.objects.get(id=block_id)
        if not block:
            return Response({"code": 400, "msg": "数据不存在"})
        
        # 翻译成英文        
        ai_data = translate(content, "trans2en")
        if ai_data.get("success"):
            text = ai_data.get("text")
    
        # return Response({"code": 200, "msg": "生成图片成功", "data": "OK"})
        prompt = text

        # 生成图片
        url = "https://23329.o.apispace.com/aigc/txt2img"
        payload = {"task": "txt2img.sd", "params": {"model": "anime", "text": prompt, "w": 512, "h": 512, "guidance_scale": 14, "negative_prompt": "cropped, blurred, mutated, error, lowres, blurry, low quality, username, signature, watermark, text, nsfw, missing limb, fused hand, missing hand, extra limbs, malformed limbs, bad hands, extra fingers, fused fingers, missing fingers, bad breasts, deformed, mutilated, morbid, bad anatomy", "sampler": "k_euler", "seed": -1, "num_steps": 25}, "model": "anime",
                   "text": "{{{ masterpiece }}}, exquisite facial features, masterpiece, perfect facial features, exquisite details, eyes, hair atmosphere, high resolution, 4K image quality, best light, delicate skin, detailed light, masterpiece, best quality,higher quality,high details, human head and deer body, sagittata, beautiful female face, long eyelashes, long silver hair, several braids, crystal bow and arrow, crystal translucent deer horn, corolla, silvery white fur wraps the whole body, no meat, crystal forest, magic, circle, masterpiece, masterpiece, ultra-high definition, countless golden light spots, dream charm, human personification, colorful light and shadow, top light, realistic effect, grade safety, unity, (ultra-fine CG:1.2),(8K:1.2), indoor, {{{{{wind blowing}}}}}}}}}} light, {{{}}}}}} {{{{{{{{{{{{{{{{{{{{{{{, 4k", "w": 512, "h": 512, "guidance_scale": 14, "negative_prompt": "cropped, blurred, mutated, error, lowres, blurry, low quality, username, signature, watermark, text, nsfw, missing limb, fused hand, missing hand, extra limbs, malformed limbs, bad hands, extra fingers, fused fingers, missing fingers, bad breasts, deformed, mutilated, morbid, bad anatomy", "sampler": "k_euler", "seed": 1072366942, "num_steps": 25, "notify_url": ""}
       
        headers = {
            "X-APISpace-Token": "1346p4ztb3ogodv9vg8qzfpyxp47siie",
            "Authorization-Type": "apikey",
            "Content-Type": "application/json"
        }

        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers)
        
        response_data = json.loads(response.text)
        print(response_data)
        """
        {
          "code": 0,
          "data": {
              "uid": "5c52c5b25c42f4a0207a88683d44429e"
            },
          "msg": "success"
        }
        """
        uid = response_data["data"]["uid"]

        # 查询图片

        url_pic = "https://23329.o.apispace.com/aigc/query-image"

        payload_pic = {"uid": uid}

        headers_pic = {
            "X-APISpace-Token": "1346p4ztb3ogodv9vg8qzfpyxp47siie",
            "Authorization-Type": "apikey",
            "Content-Type": "application/json"
        }

        response_pic = requests.request("POST", url_pic, data=json.dumps(payload_pic), headers=headers_pic)
        response_pic_data = json.loads(response_pic.text)
        print(response_pic_data)

        cdn = response_pic_data["data"]["cdn"]

        # 如cdn为空，延时100ms后再次查询,最多查询12次
        if not cdn:
            for i in range(12):
                time.sleep(0.1)
                response_pic = requests.request("POST", url_pic, data=json.dumps(payload_pic), headers=headers_pic)
                response_pic_data = json.loads(response_pic.text)
                print(response_pic_data)
                cdn = response_pic_data["data"]["cdn"]
                if cdn:
                    break

        # 保存图片
        text = {
            "url": cdn,
            "uid": uid,
        }

        block.data = {"text": text}
        block.save()

        return Response({"code": 200, "msg": "生成图片成功", "data": block.data})


    def postTest(self, request):
        block_id = request.data.get("block_id")
        content = request.data.get("content")

        block = Block.objects.get(id=block_id)
        if not block:
            return Response({"code": 400, "msg": "数据不存在"})
        
        # 翻译成英文        
  
        # return Response({"code": 200, "msg": "生成图片成功", "data": "OK"})
        prompt = content


        uid = '00492976c4cafafa137fdfd9afb51a08'
        # 查询图片

        url_pic = "https://23329.o.apispace.com/aigc/query-image"

        payload_pic = {"uid": uid}

        headers_pic = {
            "X-APISpace-Token": "1346p4ztb3ogodv9vg8qzfpyxp47siie",
            "Authorization-Type": "apikey",
            "Content-Type": "application/json"
        }

        response_pic = requests.request("POST", url_pic, data=json.dumps(payload_pic), headers=headers_pic)
        response_pic_data = json.loads(response_pic.text)
        print(response_pic_data)

        cdn = response_pic_data["data"]["cdn"]

        # 如cdn为空，延时100ms后再次查询,最多查询10次
        if not cdn:
            for i in range(10):
                time.sleep(0.1)
                response_pic = requests.request("POST", url_pic, data=json.dumps(payload_pic), headers=headers_pic)
                response_pic_data = json.loads(response_pic.text)
                print(response_pic_data)
                cdn = response_pic_data["data"]["cdn"]
                if cdn:
                    break



        block.data = {"text": cdn}
        block.save()

        return Response({"code": 200, "msg": "生成图片成功", "data": block.data})


# 返回block
"""
查询图片返回格式
{
    "code": 0,
    "data": {
        "uid": "eaab02b9d732a214ce515beca5089a46",
        "status": "finished",
        "cdn": "https://ailab-huawei-cdn.nolibox.com/aigc/images/d3eb6e64ec62400ca5db6eadd65a3ac7.png",
        "safe": true,
        "reason": "",
        "create_time": 1681976700,
        "start_time": 1681976700,
        "end_time": 1681976700,
        "duration": 4.0144863
    },
    "msg": "success"
}

"""