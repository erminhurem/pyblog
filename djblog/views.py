from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Post, Comment, PostLike


class PostListView(ListView):
    """Alternative post list view"""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 6
    template_name = 'djblog/post_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Create a dictionary of post_id -> is_liked for quick lookups
            user_likes = {like.post_id: True for like in PostLike.objects.filter(user=self.request.user)}
            for post in context['posts']:
                post.is_liked = user_likes.get(post.id, False)
        return context

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    is_liked = post.is_liked_by(request.user) if request.user.is_authenticated else False
    return render(request, 'djblog/post_detail.html', {
        'post': post,
        'comments': comments,
        'is_liked': is_liked
    })

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    
    if request.method == 'POST':
        author = request.POST.get('author')
        content = request.POST.get('content')
        
        if author and content:
            Comment.objects.create(
                post=post,
                author=author,
                content=content
            )
            messages.success(request, 'Your comment has been added successfully!')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return redirect(post.get_absolute_url())

@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        try:
            # Try to create a new like
            PostLike.objects.create(post=post, user=request.user)
            action = 'liked'
        except IntegrityError:
            # User already liked the post, so unlike it
            PostLike.objects.filter(post=post, user=request.user).delete()
            action = 'unliked'
        
        return JsonResponse({
            'likes': post.total_likes,
            'action': action
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

