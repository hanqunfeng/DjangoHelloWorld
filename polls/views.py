# Create your views here.

from django.http import Http404  # 抛出404异常
from django.http import HttpResponse, HttpResponseRedirect
# 使用render时就不需要引入HttpResponse和loader的依赖
# 使用get_object_or_404则不需要引入Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader  # 加入模板
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice


def index2(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]  # -pub_date表示倒序，正序去掉负号，[:5]取0~5
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail2(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")  # 没有查询到数据则抛出404异常
    return render(request, 'polls/detail.html', {'question': question})


def detail(request, question_id):
    # get_object_or_404()函数将一个Django模型作为它的第一个参数，任意数量的关键字参数作为它的第二个参数，
    # 它会将这些关键字参数传递给模型管理器中的get()函数。 如果对象不存在，它就引发一个Http404异常。
    # 还有一个get_list_or_404()函数，它的工作方式类似get_object_or_404()
    # 差别在于它使用filter()而不是get()。 如果列表为空则引发Http404。
    question = get_object_or_404(Question, pk=question_id)
    # render()函数将请求对象作为它的第一个参数，模板的名字作为它的第二个参数，一个字典作为它可选的第三个参数。
    # 它返回一个HttpResponse对象，含有用给定的context渲染后的模板。
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    input_img = request.FILES['photo']
    question.photo = input_img
    question.save()

    try:
        # request.POST是一个类似字典的对象，让你可以通过关键字的名字获取提交的数据。request.POST 的值永远是字符串
        # Django还以同样的方式提供request.GET用于访问GET数据
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 重新显示该问题的表单
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1  # 这样做有一个问题，就是相同时间如果有多个人投票，此时保存的votes值就是错误的
        selected_choice.save()
        # 始终在成功处理 POST 数据后返回一个 HttpResponseRedirect ，
        # 这样可以防止用户点击“后退”按钮时数据被发送两次。
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# 通用视图，与index方法对比发现，业务逻辑只有查询后返回页面，所以可以修改为这种通用视图逻辑，但总感觉不实用
class IndexView(generic.ListView):  # 继承list视图
    # 如果与默认值相同，以下两项可以不设置
    template_name = 'polls/index.html'  # 返回的模板视图路劲，默认为：app_name/model_name_list.html，比如：polls/question_list.html
    context_object_name = 'latest_question_list'  # 返回页面的对象key，默认为model_name_list，比如：question_list
    # import os
    #
    # path = os.path.abspath(__file__)
    # print(path)  # /Users/hanqunfeng/python_workspace/DjangoHelloWorld/polls/views.py
    # path = os.path.dirname(path)  # 获取父目录路径
    # print(path)  # /Users/hanqunfeng/python_workspace/DjangoHelloWorld/polls
    # path = os.path.dirname(path)
    # print(path)  # /Users/hanqunfeng/python_workspace/DjangoHelloWorld
    #
    # print("#####################################################################")
    #
    # path = os.path.dirname(__file__)
    # print("1", path)  # /Users/hanqunfeng/python_workspace/DjangoHelloWorld/polls
    # path = os.path.dirname(path)
    # print("2", path)  # /Users/hanqunfeng/python_workspace/DjangoHelloWorld
    #
    # path = os.path.abspath("")
    # print(path)  # /Users/hanqunfeng/python_workspace/DjangoHelloWorld

    def get_queryset(self):  # context_object_name的value
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]

        return Question.objects.filter(
            pub_date__lte=timezone.now()  # <=当前时间
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):  # 继承detail视图
    model = Question  # 返回detail页面的model object，默认的context_object_name为question
    template_name = 'polls/detail.html'

    def get_queryset(self):  # 限制返回结果时可以重写该方法
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):  # 继承detail视图
    model = Question
    template_name = 'polls/results.html'
