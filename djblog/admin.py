from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import Post, Comment, PostLike

class EngagementFilter(admin.SimpleListFilter):
    title = 'engagement level'
    parameter_name = 'engagement'

    def lookups(self, request, model_admin):
        return (
            ('high', 'High (10+ likes)'),
            ('medium', '5-10 likes'),
            ('low', 'Less than 5 likes'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'high':
            return queryset.annotate(like_count=Count('post_likes')).filter(like_count__gte=10)
        if self.value() == 'medium':
            return queryset.annotate(like_count=Count('post_likes')).filter(like_count__gte=5, like_count__lt=10)
        if self.value() == 'low':
            return queryset.annotate(like_count=Count('post_likes')).filter(like_count__lt=5)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', 'total_likes', 'total_comments', 'engagement_rate']
    list_filter = ['status', 'publish', 'author', EngagementFilter]
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS
    actions = ['export_as_csv', 'mark_as_published', 'mark_as_draft']
    change_list_template = 'admin/post/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                'engagement-stats/',
                self.admin_site.admin_view(self.engagement_stats_view),
                name='djblog_post_engagement_stats',
            ),
        ]
        return my_urls + urls

    def engagement_stats_view(self, request):
        from django.db.models import Avg, Max
        stats = {
            'total_posts': Post.objects.count(),
            'total_likes': PostLike.objects.count(),
            'total_comments': Comment.objects.count(),
            'avg_likes_per_post': Post.objects.annotate(like_count=Count('post_likes')).aggregate(Avg('like_count'))['like_count__avg'] or 0,
            'most_liked_post': Post.objects.annotate(like_count=Count('post_likes')).order_by('-like_count').first(),
            'most_commented_post': Post.objects.annotate(comment_count=Count('comments')).order_by('-comment_count').first(),
        }
        from django.shortcuts import render
        return render(request, 'admin/post/engagement_stats.html', stats)

    def total_likes(self, obj):
        url = f"/admin/djblog/postlike/?post__id={obj.id}"
        return format_html('<a href="{}">{}</a>', url, obj.post_likes.count())
    total_likes.short_description = 'Likes'

    def total_comments(self, obj):
        url = f"/admin/djblog/comment/?post__id={obj.id}"
        return format_html('<a href="{}">{}</a>', url, obj.comments.count())
    total_comments.short_description = 'Comments'

    def engagement_rate(self, obj):
        total_engagement = obj.post_likes.count() + obj.comments.count()
        if total_engagement > 10:
            color = 'green'
        elif total_engagement > 5:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {}">{}</span>', color, total_engagement)
    engagement_rate.short_description = 'Engagement'

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = ['title', 'author', 'publish', 'status', 'total_likes', 'total_comments']
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.model_name}_{datetime.now().strftime("%Y%m%d")}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = [getattr(obj, field) if field not in ['total_likes', 'total_comments'] 
                  else (obj.post_likes.count() if field == 'total_likes' else obj.comments.count())
                  for field in field_names]
            writer.writerow(row)

        return response
    export_as_csv.short_description = "Export selected posts as CSV"

    def mark_as_published(self, request, queryset):
        queryset.update(status=Post.Status.PUBLISHED)
    mark_as_published.short_description = "Mark selected posts as published"

    def mark_as_draft(self, request, queryset):
        queryset.update(status=Post.Status.DRAFT)
    mark_as_draft.short_description = "Mark selected posts as draft"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('post_likes', 'comments')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created', 'active', 'short_content']
    list_filter = ['active', 'created', 'post']
    search_fields = ['author', 'content', 'post__title']
    actions = ['approve_comments', 'disapprove_comments', 'export_as_csv']
    list_per_page = 20

    def short_content(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    short_content.short_description = 'Content Preview'

    def approve_comments(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f'{updated} comments were successfully approved.')
    approve_comments.short_description = 'Approve selected comments'

    def disapprove_comments(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, f'{updated} comments were successfully disapproved.')
    disapprove_comments.short_description = 'Disapprove selected comments'

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = ['post', 'author', 'content', 'created', 'active']
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=comments_{datetime.now().strftime("%Y%m%d")}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = [str(getattr(obj, field)) for field in field_names]
            writer.writerow(row)

        return response
    export_as_csv.short_description = "Export selected comments as CSV"

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created', 'post_title']
    list_filter = ['created', 'user', 'post']
    search_fields = ['post__title', 'user__username', 'user__email']
    raw_id_fields = ['post', 'user']
    date_hierarchy = 'created'
    actions = ['export_as_csv']

    def post_title(self, obj):
        return obj.post.title
    post_title.short_description = 'Post Title'
    post_title.admin_order_field = 'post__title'

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = ['post', 'user', 'created']
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=likes_{datetime.now().strftime("%Y%m%d")}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = [str(getattr(obj, field)) for field in field_names]
            writer.writerow(row)

        return response
    export_as_csv.short_description = "Export selected likes as CSV"

