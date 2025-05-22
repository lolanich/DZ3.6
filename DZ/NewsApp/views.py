import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .forms import NewsForm, ArticleForm
from .models import Post, Category
from .filter import NewsFilter
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = '-dateCreations'
    template_name = 'post.html'
    context_object_name = 'post'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class NewsCreate(CreateView, PermissionRequiredMixin):
    permission_required = '<NewsApp>.<add>_<post>'
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'news'
        post.save()
        return super().form_valid(form)


class ArticleCreate(CreateView, PermissionRequiredMixin):
    permission_required = '<NewsApp>.<add>_<post>'
    form_class = ArticleForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'article'
        post.save()
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    permission_required = '<NewsApp>.<change>_<post>'
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, categoryType='news', id=self.kwargs['pk'])


class ArticleUpdate(LoginRequiredMixin, UpdateView,  PermissionRequiredMixin):
    permission_required = '<NewsApp>.<change>_<post>'
    form_class = ArticleForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, categoryType='article', id=self.kwargs['pk'])


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, categoryType='news', id=self.kwargs['pk'])


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, categoryType='article', id=self.kwargs['pk'])


def search_news(request):
    query = request.GET.get('query', '')
    author = request.GET.get('author', '')
    date_after = request.GET.get('date_after', '')

    posts_queryset = Post.objects.all()

    if query:
        posts_queryset = posts_queryset.filter(title__icontains=query)

    if author:
        posts_queryset = posts_queryset.filter(
            author__name__icontains=author)

    if date_after:
        posts_queryset = posts_queryset.filter(dateCreations__gte=date_after)

    context = {
        'posts': posts_queryset,
        'query': query,
        'author': author,
        'date_after': date_after,
    }

    return render(request, 'post_search.html', context)



