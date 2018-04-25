from django.urls import path, re_path

from . import views  # 导入当前应用下的视图信息

app_name = 'django2'  # 设置命名空间

urlpatterns = [
    # ex: /django2/
    path('books/', views.book_index, name='book_index'),
    # ex: /django2/books/5/
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/delete/<int:book_id>/', views.book_delete, name='book_delete'),
    path('books/save/', views.book_save, name='book_save'),
    path('books/json', views.book_query_json, name='book_query_json'),

]
