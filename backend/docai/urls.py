
from django.urls import path
from rest_framework import routers
from docai.views import doc, knowledgeBase, textAI


doc_url = routers.DefaultRouter()
doc_url.register(r'page', doc.PageViewSet)
doc_url.register(r'block', doc.BlockViewSet)
doc_url.register(r'knowledge', knowledgeBase.KnowledgeViewSet)

doc_url.register(r'block_ai', textAI.BlockViewSet)  # 块级AI操作



urlpatterns = [
    

]

urlpatterns += doc_url.urls  # 将路由器中的所以路由信息追加到django的路由列表中


