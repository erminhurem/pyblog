from django.contrib import admin
from .models import Post, Comment, PostLike

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', 'total_likes', 'total_comments']
    list_filter = ['status', 'publish', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS

    def total_likes(self, obj):
        return obj.post_likes.count()
    total_likes.short_description = 'Likes'

    def total_comments(self, obj):
        return obj.comments.count()
    total_comments.short_description = 'Comments'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('post_likes', 'comments')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created', 'active']
    list_filter = ['active', 'created']
    search_fields = ['author', 'content']
    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = 'Approve selected comments'

    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)
    disapprove_comments.short_description = 'Disapprove selected comments'


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created']
    list_filter = ['created', 'user']
    search_fields = ['post__title', 'user__username']
    raw_id_fields = ['post', 'user']
    date_hierarchy = 'created'

