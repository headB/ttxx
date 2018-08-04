from django.contrib import admin
from goods.models import Goods,GoodsSKU,GoodsType,IndexPromotionBanner,IndexGoodsBanner,IndexTypeGoodsBanner
# Register your models here.
##导入类,用于一旦管理员操作了数据,就进行把数据更新
from django.core.cache import cache
#admin.site.register(GoodsType)

class BaseModelAdmin(admin.ModelAdmin):

    def save_model(self,request,obj,form,change):
        '''新增或者更新表仲的数据时调用'''
        super().save_model(request,obj,form,change)

        #发出任务,让celery_worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        #清除首页的缓存数据
        cache.delete('index_page_data')

    def delete_model(self,request,obj):
        '''删除表中的数据时的调用'''
        super().delete_model(request,obj)

        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

         #清除首页的缓存数据
        cache.delete('index_page_data')

#写新类
class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass

class GoodsTypeAdmin(BaseModelAdmin):
    pass

class IndexGoodsBannerAdmin(BaseModelAdmin):
    pass

class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    pass

class GoodsAdmin(BaseModelAdmin):
    pass

class GoodsSKUAdmin(BaseModelAdmin):
    pass






admin.site.register(Goods,GoodsAdmin)
admin.site.register(GoodsSKU,GoodsSKUAdmin)

admin.site.register(IndexPromotionBanner,IndexPromotionBannerAdmin)
admin.site.register(GoodsType,GoodsTypeAdmin)
admin.site.register(IndexGoodsBanner,IndexGoodsBannerAdmin)
admin.site.register(IndexTypeGoodsBanner,IndexTypeGoodsBannerAdmin)