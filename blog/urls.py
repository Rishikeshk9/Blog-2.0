from django.urls import path
from django.conf.urls import url
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, PostLikeToggle, ChartView, get_data, ChartData
from . import views

urlpatterns = [
    path("", PostListView.as_view(), name="blog-home"),
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path('like/<int:pk>',PostLikeToggle.as_view() , name="uplike"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("about/", views.about, name="blog-about"),
    path("blog/chart/",ChartView.as_view(), name="charts"),
    url(r"^api/data/$",get_data, name="api-data"),
    url(r"^api/chart/data/$",ChartData.as_view()),
]
