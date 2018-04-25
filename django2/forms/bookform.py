from django import forms


class BookForm(forms.Form):
    bookname = forms.CharField(label='书名', max_length=100, help_text='请输入书名', required=True)
    bookpapers = forms.IntegerField(label='页数', min_value=1)
    author = forms.CharField(label='作者', max_length=20)
    # class Meta:
    #     model = Book
    #     fields = ('id', 'bookname', 'bookpapers', 'author')
