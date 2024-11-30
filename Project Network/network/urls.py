
from django.urls import path

from . import views

from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post", views.new_post , name="new-post"),
    path('all-posts',views.all_posts,name="all-posts"),
    path('profile/<str:username>/', views.profile_view, name="profile"),
    path('edit_post/<int:post_id>/',views.edit_post,name="edit_post"),
    path('like_unlike_post/<int:post_id>/',views.like_unlike_post,name="like_unlike_post"),
    path('following',views.following_page,name="following"),
    path('profile/image-upload/', views.image, name='profile-image-upload'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('add_comment/<int:post_id>/',views.add_comment,name="add_comment"),
    path('profile/image-upload/',views.upload_profile_image,name="profile-image-upload")
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)