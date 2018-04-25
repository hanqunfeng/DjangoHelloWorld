from django.contrib import admin

from .models.car import Car
from .models.identity_card import IdentityCard
from .models.user import User


# Register your models here.

class IdentityCardInline(admin.TabularInline):
    model = IdentityCard
    extra = 1  # 因为是1to1，所以编辑页面重新打开时不会增加新的一行的


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['birth_day']}),
        (None, {'fields': ['phone']}),
        (None, {'fields': ['email']}),
    ]

    inlines = [IdentityCardInline]
    list_display = ('name', 'birth_day', 'phone', 'email')  # 列表显示哪些字段和方法
    list_filter = ['name', 'email']  # 页面右侧增加过滤器
    search_fields = ['name', 'email']  # 查询字段
    list_per_page = 10  # 每页显示行数


class CarAdmin(admin.ModelAdmin):
    list_display = ('carNum', 'carColor', 'carPrice')
    list_filter = ['carNum', 'carColor']
    search_fields = ['carNum', 'carColor']  # 查询字段
    list_per_page = 10  # 每页显示行数


admin.site.register(User, UserAdmin)
# admin.site.register(IdentityCard) # 上面已经配置了在user的创建页面中就可以直接创建身份证号，所以没必要单独开启维护功能
admin.site.register(Car, CarAdmin)
