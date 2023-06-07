from django.db import models



class CoreModel(models.Model):
    """
    核心标准抽象模型模型,可直接继承使用
    """
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        abstract = True     #abstract 这个属性是定义当前模型类是不是一个抽象类
        verbose_name = '核心模型'
        verbose_name_plural = verbose_name


"""主页模型  暂时不用
class Home(CoreModel):
  
    page_seq = models.JSONField(null=True, blank=True, verbose_name="页面次序", help_text="页面次序")  # 数据结构 [page_id, page_id, ...]

    class Meta:
        verbose_name = "主页表"
        verbose_name_plural = verbose_name
"""


def default_list():
    return []


def upload_cover(instance, filename):
    """封面上传"""
    return 'note/cover/%s/%s' % (instance.id, filename)


class Page(CoreModel):
    """页面模型"""
    title = models.CharField(max_length=120, null=True, blank=True, verbose_name="标题", help_text="标题")
    icon = models.CharField(max_length=100, null=True, blank=True, verbose_name="icon", help_text="icon")
    cover = models.ImageField(upload_to=upload_cover, null=True, blank=True, verbose_name="封面", help_text="封面")
    # home = models.ForeignKey(to="Home", on_delete=models.CASCADE, db_constraint=False, null=True, blank=True, verbose_name="所属主页", help_text="所属主页")
    block_seq = models.JSONField(default=default_list,  null=True, blank=True, verbose_name="块次序", help_text="块次序")  # 数据结构 [Block_id, Block_id, ...]

    class Meta:
        verbose_name = "笔记页表"
        verbose_name_plural = verbose_name


class Block(CoreModel):
    """块模型"""
    type = models.CharField(max_length=120, null=True, blank=True, verbose_name="类型", help_text="类型")
    data = models.JSONField(null=True, blank=True, verbose_name="数据", help_text="数据")
    page = models.ForeignKey(to="Page", on_delete=models.CASCADE, db_constraint=False, null=True, blank=True, verbose_name="所属页面", help_text="所属页面")

    class Meta:
        verbose_name = "Block表"
        verbose_name_plural = verbose_name



### 知识库相关模型 ###

def upload_file(instance, filename):
    """封面上传"""
    #时间戳+文件后缀
    import time
    tag = str(int(time.time()))
    return 'note/file/%s/%s' % (tag, filename)



class Knowledge(CoreModel):

    name = models.CharField(max_length=120, null=True, blank=True, verbose_name="文档名称", help_text="文档名称")
    type = models.CharField(max_length=120, null=True, blank=True, verbose_name="文档类型", help_text="文档类型")
    file = models.FileField(upload_to=upload_file, null=True, blank=True, verbose_name="文档", help_text="文档")



