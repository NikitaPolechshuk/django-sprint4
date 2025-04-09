from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, DeleteView
)

from .models import Post, Category, Comment
from .forms import (
    PostForm, CommentForm
)


PAGINATOR_NUM = 10


User = get_user_model()


def get_base_post_queryset():
    """Базовый запрос к модели Post."""
    return Post.objects.select_related(
        'location', 'author', 'category',
    ).annotate(
        comment_count=Count('post_comments')
    ).order_by('-pub_date')


def base_filter_queryset(queryset):
    """Базовая фильтрация."""
    return queryset.filter(pub_date__lte=timezone.now(),
                           category__is_published=True,
                           is_published=True)


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostMixin:
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    queryset = get_base_post_queryset()


class CommentMixin:
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class BasePostListView(PostMixin, ListView):
    paginate_by = PAGINATOR_NUM

    class Meta:
        abstract = True


class PostListView(BasePostListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return base_filter_queryset(queryset)


class UserPostListView(BasePostListView):
    template_name = 'blog/profile.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(User,
                                               username=self.kwargs['username']
                                               )
        return context


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user})


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_queryset(self):
        base_queryset = super().get_queryset()
        filtered_base_queryset = base_filter_queryset(base_queryset)
        if self.request.user.is_authenticated:
            # Если пользователь авторизован, то ему доступны
            # все его записи
            return filtered_base_queryset | base_queryset.filter(
                author=self.request.user)
        # Для пользователя без авторизации возвращаем
        # QuerySet с базовой фильтрацией
        return filtered_base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.select_related().filter(
            post_id=self.kwargs['post_id']
        )
        return context


class PostUpdateView(OnlyAuthorMixin, PostMixin, UpdateView):
    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.kwargs['post_id']})


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    template_name = 'blog/post_delete.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        queryset = get_base_post_queryset()
        return queryset.filter(pk=self.kwargs['post_id'])

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user})


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.kwargs['post_id']}
                            )

    def form_valid(self, form):
        # Если поста не существуем, выбрасываем 404
        get_object_or_404(Post, pk=self.kwargs['post_id'])
        # Заполняем форму
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)


class CommentUpdateView(OnlyAuthorMixin, CommentMixin, UpdateView):
    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.kwargs['post_id']})


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.kwargs['post_id']})


class CategoryPostListView(BasePostListView):
    template_name = 'blog/category.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return base_filter_queryset(queryset).filter(
            category__slug=self.kwargs['category_slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True)
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ['username', 'first_name', 'last_name', 'email']

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.object.username})
