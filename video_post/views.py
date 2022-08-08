from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import VideoPost
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

# Create your views here.
def home(request):
    context = {
        'videos': VideoPost.objects.all()
    }
    return render(request, 'video_post/home.html', context)


class PostListView(ListView):
    model = VideoPost  #It will tell out list what model to query
    template_name = 'video_post/home.html'
    context_object_name = 'videos'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = VideoPost  #It will tell out list what model to query
    template_name = 'video_post/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    # def get_queryset(self):
    #     user = get_object_or_404(get_user_model(), email=self.kwargs.get('email'))
    #     return VideoPost.objects.filter(creator=user).order_by('-date_posted')

    def get_context_data(self, *args, **kwargs):
        context = super(UserPostListView, self).get_context_data(*args, **kwargs)
        user = get_object_or_404(get_user_model(), email=self.kwargs.get('email'))
        posts = VideoPost.objects.filter(creator=user).order_by('-date_posted')
        context['posts'] = posts
        context['other_user'] = user
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = VideoPost  #It will tell out list what model to query
    fields = ['title', 'content', 'description']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = VideoPost
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView,
             self).get_context_data(*args, **kwargs)
        # add extra field
        likes = get_object_or_404(VideoPost, id=self.kwargs['pk'])
        total_likes = likes.total_likes()
        dislikes = get_object_or_404(VideoPost, id=self.kwargs['pk'])
        total_dislikes = dislikes.total_dislikes()
        context["total_likes"] = total_likes
        context["total_dislikes"] = total_dislikes
        return context


class SearchResultsView(ListView):
    model = VideoPost
    template_name = "video_post/search_result.html"
    # context_object_name = 'search_result'

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = VideoPost.objects.filter(
            Q(title__icontains=query)
        )
        return object_list


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VideoPost  #It will tell out list what model to query
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.creator:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VideoPost  #It will tell out list what model to query
    fields = ['title', 'content', 'description']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.creator:
            return True
        return False


def LikeView(request, pk):
    post = get_object_or_404(VideoPost, id=request.POST.get('post_id'))
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def DislikeView(request, pk):
    post = get_object_or_404(VideoPost, id=request.POST.get('post_id'))
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))