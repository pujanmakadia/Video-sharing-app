from django.urls import path
from .views import (
    PostCreateView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SearchResultsView,
    LikeView,
    DislikeView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='posts-home'),
    path("search/", SearchResultsView.as_view(), name="search_result"),
    path('user/<str:email>/', UserPostListView.as_view(), name='user-posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:pk>/', LikeView, name='like-post'),
    path('dislike/<int:pk>/', DislikeView, name='dislike-post'),
]