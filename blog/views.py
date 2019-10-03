from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from hitcount.views import HitCountDetailView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView, View
import random
from .models import Post

def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", {customers: '100'})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <appp>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <appp>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True


class PostLikeToggle(RedirectView):

    def get_redirect_url(self, *args ,**kwargs):

        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        url_ = obj.get_absolute_url() 
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                # you could remove the user if double upvote or display a message or what ever you want here
                obj.likes.remove(user)
            else:
                obj.likes.add(user)

        return url_


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", {"title": "About"})


class ChartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/charts.html',{})

def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customer": 10,
    }
    return JsonResponse(data)

class ChartData(APIView):
    """
    View to list all users in the system.
    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format1=None):
        qs_count = User.objects.all().count()
        labels = [user.username for user in User.objects.all()]
        default_items = [Post.objects.filter(author=user).count() for user in User.objects.all()]
        colors=[]
        for user in User.objects.all():
            color ='rgba('+format(random.randint(0,255))+","+format(random.randint(0,255))+","+format(random.randint(0,255))+",1)"
            colors.append(color)
        #color = 'rgba('+format(random.randint(0,255))+","+format(random.randint(0,255))+","+format(random.randint(0,255))+",1)"
        data = {
                 "labels": labels,
                 "default": default_items,
                 "bgcolor": colors,
                }
        ##usernames = [user.username for user in User.objects.all()]
        return Response(data)