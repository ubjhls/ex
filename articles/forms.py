from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('__all__')
        exclude = ('article', )



# class ArticleForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = '__all__'
        # fields = ('title')
        # exclude = ('title')
        # widgets = {
        #     'title': forms.TextInput(
        #         attrs={
        #             'placeholder': '제목을 입력바랍니다.'
        #         }
        #     )
        # }



# class ArticleForm(forms.Form):
#     title = forms.CharField(
#         max_length=1, 
#         label='제목',
#         widget=forms.TextInput(
#             attrs={
#                 'placeholder':'제목을 입력바랍니다.'
#             }
#         )
#     )
#     content = forms.CharField(
#         # label 내용 수정
#         label='내용',
#         # Django form 에서 HTML 속성 지정 -> widget
#         widget=forms.Textarea(
#             attrs={
#                 'class': 'my-content',
#                 'placeholder': '내용을 입력바랍니다.',
#                 'row': 5,
#                 'cols': 60,
#             }
#         )
#     )