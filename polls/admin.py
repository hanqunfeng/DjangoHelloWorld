from django.contrib import admin

from .models import Question, Choice


# Register your models here.
# 管理后台可以维护注册的表
# admin.site.register(Question)

# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        (None, {'fields': ['photo']}),
        (None, {'fields': ['uploadfile']}),
    ]
    inlines = [ChoiceInline]

    list_display = ('question_text', 'pub_date', 'was_published_recently')  # 列表显示哪些字段和方法
    list_filter = ['pub_date']  # 页面右侧增加过滤器
    search_fields = ['question_text']  # 查询字段
    list_per_page = 10  # 每页显示行数


admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)
