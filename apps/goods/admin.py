from django.contrib import admin
from goods.models import GoodsType,IndexPromotionBanner
# Register your models here.

#admin.site.register(GoodsType)

#写新类
class IndexPromotionBannerAdmin(admin.ModelAdmin):
    def save_model(self,request,obj,form,change):
        '''新增或者更新表仲的数据时调用'''
        super().save_model(request,obj,form,change)

    #发出任务,让celery_worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

    def delete_model(self,request,obj):
        '''删除表中的数据时的调用'''
        super().delete_model(request,obj)
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

admin.site.register(GoodsType)
admin.site.register(IndexPromotionBanner,IndexPromotionBannerAdmin)