import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .forms import NewsForm, ArticleForm
from .models import Post
from .filter import NewsFilter
from django.shortcuts import get_object_or_404


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


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'news'
        post.save()
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'article'
        post.save()
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, categoryType='news', id=self.kwargs['pk'])


class ArticleUpdate(UpdateView):
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