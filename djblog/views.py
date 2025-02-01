from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from .models import Post


class PostListView(ListView):
    """Alternative post list view"""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'djblog/post_list.html'
    

def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) # If page is out of range (e.g. 9999), deliver last page of results.
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'djblog/post_detail.html', {'post': post})

