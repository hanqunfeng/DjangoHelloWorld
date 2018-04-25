from django.urls import path

from . import views  # 导入当前应用下的视图信息

app_name = 'polls'  # 设置命名空间

# 定义请求路径与视图的映射规则，url,视图处理方法,视图名称
# urlpatterns = [
#     # ex: /polls/
#     path('', views.index, name='index'),
#     # ex: /polls/5/
#     path('<int:question_id>/', views.detail, name='detail'),
#     # ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]



# path()函数传递四个参数，两个必选参数：regex和view，两个可选参数：kwargs和name。
# path()参数：route
# 在这里是匹配url。 Django从第一个正则表达式开始，在列表中自上而下匹配，将请求的URL与每个正则表达式进行比较，直到找到匹配的一个。
#
# 请注意，这些正则表达式不搜索GET和POST参数或域名。 例如，在https://www.example.com/myapp/的请求中，URLconf将查找myapp/。
# 在https://www.example.com/myapp/?page=3的请求中，URLconf仍将查找myapp/。
#
# 如果你需要正则表达式的帮助，请参阅维基百科的条目和re模块的文档。 此外，由Jeffrey Friedl撰写的O'Reilly书“精通正则表达式”非常棒。
# 但实际上，你不需要成为正则表达式的专家，因为你只需要知道如何捕获简单的模式。 实际上，复杂的正则表达式的查找性能可能很差，所以你可能不应该依靠正则表达式的全部功能。
#
# 最后，一个性能提示：这些正则表达式是第一次加载URLconf模块时被编译。 它们超级快（只要查找不是太复杂，如上所述）。
#
# path()参数：view 当Django发现正则表达式匹配时，Django将调用指定的视图函数，使用HttpRequest对象作为第一个参数，并将正则表达式中的任何“捕获”值作为其他参数。
# 如果正则表达式使用简单的捕获，则值作为位置参数传递；如果它使用命名捕获，则值作为关键字参数传递。 我们稍后会给出一个例子。
#
# path()参数：kwargs
# 任意关键词参数可以在字典中传递到目标视图。 我们不会在该教程中使用Django的这个功能。
#
# path()参数：name
# 命名你的URL可让你从Django其他地方明确地引用它，特别是在模板中。 这个强大的功能允许你在仅接触单个文件的情况下对项目的URL模式进行全局更改。


# 通用视图，这个概念不太好理解，只倾向于业务逻辑比较简单的list和detail
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]


# 我们在这里使用两个通用视图：ListView 和 DetailView。
# 这两个视图分别抽象“显示一个对象列表”和“显示一个特定类型对象的详细信息页面”这两种概念。
#
# 每个通用视图需要知道它将作用于哪个模型。 这由model 属性提供。
# DetailView期望从URL中捕获名为"pk"的主键值，因此我们把polls/urls.py中question_id改成了pk以使通用视图可以找到主键值 。
# 默认情况下，通用视图DetailView 使用一个叫做<app name>/<model name>_detail.html的模板。
# 在我们的例子中，它将使用 "polls/question_detail.html"模板。
# template_name属性是用来告诉Django使用一个指定的模板名字，而不是自动生成的默认名字。
# 我们也为template_name列表视图指定了results —— 这确保results视图和detail视图在渲染时具有不同的外观，即使它们在后台都是同一个 DetailView。
#
# 类似地，ListView通用视图使用名为<app name>/<model name>_list.html的；我们使用template_name来告诉ListView使用我们现有的"polls/index.html"模板。
#
# 在之前的教程中，提供模板文件时都带有一个包含question 和 latest_question_list 变量的context。
# 对于Question ，DetailView变量会自动提供—— 因为我们使用Django 的模型 (question)， Django 能够为context 变量决定一个合适的名字。
# 然而对于ListView， 自动生成的context 变量是question_list。
# 为了覆盖这个行为，我们提供 context_object_name 属性，表示我们想使用latest_question_list。
# 作为一种替换方案，你可以改变你的模板来匹配新的context变量 —— 但直接告诉Django使用你想要的变量会省事很多。

