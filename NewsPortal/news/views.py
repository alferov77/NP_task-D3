from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import Post
from .filters import NewsFilter
from .forms import PostForm

class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='NW').order_by('-creation_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_queryset(self):
        return Post.objects.filter(post_type='NW')


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = 'news/post_form.html'

    def form_valid(self, form):
        form.instance.post_type = 'NW' if 'news' in self.request.path else 'AR'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news_list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def form_valid(self, form):
        form.instance.post_type = 'NW' if 'news' in self.request.path else 'AR'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')


def search_news(request):
    news_list = Post.objects.all()
    news_filter = NewsFilter(request.GET, queryset=news_list)
    return render(request, 'news/search_news.html', {'filter': news_filter})
