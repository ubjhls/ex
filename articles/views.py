# from IPython import embed
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET

from .models import Article, Comment
from .forms import ArticleForm, CommentForm

# Create your views here.
@require_GET
def index(request):
    articles = Article.objects.order_by('-id')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

# def new(request):
#     return render(request, 'articles/new.html')

def create(request):
    # 저장 로직
    if request.method == 'POST':
        # title = request.POST.get('title')
        # content = request.POST.get('content')
        article_form = ArticleForm(request.POST,request.FILES)
        # 검증
        if article_form.is_valid():
        # 검증에 성공하면 저장하고,
            # title = article_form.cleaned_data.get('title')
            # content = article_form.cleaned_data.get('content')
            # article = Article(title=title, content=content)
            article = article_form.save()
            return redirect('articles:detail', article.pk)
        #else:
            # 다시 폼으로 돌아가 -> 중복되서 제거!
    else:
    # GET 요청 -> Form
        article_form = ArticleForm()
    # GET -> 비어있는 Form context
    # POST -> 검증 실패시 에러메세지와 입력값 채워잔 Form context
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html',context)

def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comment_set.all()
    comment_form = CommentForm()
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'articles/detail.html', context)

@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # if request.method == 'POST':
    article.delete()
    # messages.add_message(request, messages.INFO, '댓글이 삭제되었습니다.')
    messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('articles:index')
    # else:
    #     return redirect('articles:detail', article.pk)

# def edit(request, article_pk):
#     article = Article.objects.get(pk=article_pk)
#     context = {
#         'article': article
#     }
#     return render(request, 'articles/edit.html', context)

def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article) #수정할때 instance 필요
        if article_form.is_valid():
            article = article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)

@require_POST
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # 1. modelform에 사용자 입력값 넣고
    comment_form = CommentForm(request.POST)
    # 2. 검증하고,
    if comment_form.is_valid():
    # 3. 맞으면 저장!
        # 3-1. 사용자 입력값으로 comment instance 생성 (저장은 X)
        comment = comment_form.save(commit=False)
        # 3-2. FK 넣고 저장
        comment.article = article
        comment.save()
    # 4. return redirect
    else:
        messages.success(request, '댓글이 형식이 맞지않습니다.')
    return redirect('articles:detail', article_pk)
    # comment = Comment()
    # comment.content = request.POST.get('comment_content')
    # comment.article = article
    # # comment.article_id = article_pk
    # comment.save()
    # return redirect('articles:detail', article_pk)

@require_POST
def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('articles:detail', article_pk)
