from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import login
from taggit.models import Tag
from .models import Post, Comment, PostLike
from .forms import CustomUserCreationForm, UserProfileForm
from django.db import models


class PostListView(ListView):
    """Alternative post list view"""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 6
    template_name = 'djblog/post_list.html'   
    
    def get_queryset(self):
        queryset = Post.published.all()
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            try:
                tag = get_object_or_404(Tag, slug=tag_slug)
                queryset = queryset.filter(tags__in=[tag])
            except Tag.DoesNotExist:
                return Post.published.none()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Create a dictionary of post_id -> is_liked for quick lookups
            user_likes = {like.post_id: True for like in PostLike.objects.filter(user=self.request.user)}
            for post in context['posts']:
                post.is_liked = user_likes.get(post.id, False)
        
        # Add tag information if we're filtering by tag
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            try:
                tag = get_object_or_404(Tag, slug=tag_slug)
                context['current_tag'] = tag
            except Tag.DoesNotExist:
                pass
        
        return context

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    is_liked = post.is_liked_by(request.user) if request.user.is_authenticated else False
    
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=models.Count('tags')).order_by('-same_tags', '-publish')[:3]
    
    return render(request, 'djblog/post_detail.html', {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'similar_posts': similar_posts
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        
        if content:
            Comment.objects.create(
                post=post,
                author=request.user.username,
                content=content
            )
            messages.success(request, 'Your comment has been added successfully!')
        else:
            messages.error(request, 'Please enter your comment.')
    
    return redirect(post.get_absolute_url())

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user is the author
    if comment.author != request.user.username:
        messages.error(request, 'You can only edit your own comments.')
        return redirect(comment.post.get_absolute_url())
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
            messages.success(request, 'Comment updated successfully!')
        else:
            messages.error(request, 'Comment cannot be empty.')
        return redirect(comment.post.get_absolute_url())
    
    return JsonResponse({
        'content': comment.content
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user is the author
    if comment.author != request.user.username:
        messages.error(request, 'You can only delete your own comments.')
        return redirect(comment.post.get_absolute_url())
    
    if request.method == 'POST':
        post_url = comment.post.get_absolute_url()
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect(post_url)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

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

def register(request):
    if request.user.is_authenticated:
        return redirect('djblog:post_list')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('djblog:post_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_profile(request):
    user = request.user
    comments = Comment.objects.filter(author=user.username).order_by('-created')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('djblog:user_profile')
    else:
        form = UserProfileForm(instance=user)
    
    context = {
        'user': user,
        'form': form,
        'comments': comments,
    }
    return render(request, 'djblog/user_profile.html', context)

