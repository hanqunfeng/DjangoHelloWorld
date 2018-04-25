from django.urls import path, re_path

from . import views  # 导入当前应用下的视图信息

app_name = 'myapp'  # 设置命名空间

urlpatterns = [
    # ex: /myapp/
    path('users/', views.user_index, name='user_index'),
    # ex: /myapp/users/5/
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('users/save/', views.user_save, name='user_save'),
    path('users/save/', views.user_save, name='user_save'),
    re_path('users/get/(?P<year>[0-9]{4})/', views.user_index_query, name='user_index_year'),
    re_path('users/get/(?P<name>[\w]+)/', views.user_index_query, name='user_index_name'),

    path('cars/', views.car_index, name='car_index'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/delete/<int:car_id>/', views.car_delete, name='car_delete'),
    path('cars/save/', views.car_save, name='car_save'),



    path('users/json/', views.user_query_json, name='user_query_json'),
    path('users/json/<int:user_id>/', views.user_query_json_get, name='user_query_json_get'),
]
