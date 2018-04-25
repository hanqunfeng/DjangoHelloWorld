# Create your views here.
from django.db import transaction
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from django2.forms.bookform import BookForm
from django2.models.book import Book


def book_index(request):
    book_list = Book.objects.order_by('-id')[:10]

    context = {'book_list': book_list}

    return render(request, 'django2/book/index.html', context)


def book_detail(request, book_id):
    if book_id == 0:
        form = BookForm()
    else:
        try:
            book = Book.objects.get(pk=book_id)
            form = BookForm(book)
        except Book.DoesNotExist:
            raise Http404("book does not exist")  # 没有查询到数据则抛出404异常
    return render(request, 'django2/book/detail.html', {'form': form, 'id': book_id})


# 只允许接收post请求
@require_http_methods(["POST"])  # @require_http_methods(["POST","GET"]) 同时支持get和post
# 关闭csrf验证
@csrf_exempt
@transaction.atomic  # 开启事务
def book_save(request):
    # id = request.POST['id'] #这种方式取参数，当参数不存在时会报错，推荐使用下面的方式获取参数，并设置默认值

    id = request.POST.get('id', None)  # id参数不存在时设置为None
    if id and id != '0':
        book = Book.objects.get(pk=id)

    else:
        book = Book()

    form = BookForm(request.POST)
    if form.is_valid():
        book.bookname = form.cleaned_data['bookname']
        book.bookpapers = form.cleaned_data['bookpapers']
        book.author = form.cleaned_data['author']

        book.save()
    return redirect('django2:book_detail', book_id=book.id)


def book_delete(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("user does not exist")  # 没有查询到数据则抛出404异常

    book.delete()

    return HttpResponseRedirect(reverse('django2:book_index'))


from django.core import serializers


def book_query_json(request):
    book_list = Book.objects.all()
    book_list = serializers.serialize("json", book_list)
    context = {'book_list': book_list}
    return JsonResponse(context)
