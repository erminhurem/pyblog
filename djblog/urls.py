from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from . import views
from .forms import CustomAuthenticationForm
from .sitemaps import PostSitemap
from .feeds import LatestPostsFeed

app_name = 'djblog'

sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='posts_by_tag'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        form_class=CustomAuthenticationForm,
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='registration/logged_out.html',
        next_page='djblog:post_list'
    ), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/password_reset/done/'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]