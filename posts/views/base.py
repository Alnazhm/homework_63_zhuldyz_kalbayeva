from django.shortcuts import redirect
from django.views.generic import ListView
from django.db.models import Q
from posts.models import Post
from accounts.forms import SearchForm
from accounts.models import Account
from accounts.forms import CommentForm
from posts.models import Comment


class PostsIndexView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts'
    answer = 'post'

    def get(self, request, *args, **kwargs):
        self.form = SearchForm(self.request.GET)
        if self.form.is_valid():
            self.search_value = self.form.cleaned_data.get('search')
        return super().get(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True)
        if self.search_value:
            queryset = Account.objects.filter(Q(username__icontains=self.search_value) | Q(email__icontains=self.search_value))
            if len(queryset) == 0:
                self.answer = 'no'
            else:
                self.answer = 'yes'
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostsIndexView, self).get_context_data(object_list=object_list, **kwargs)
        user = self.request.user
        subscriptions = user.subscriptions.all()
        posts = Post.objects.filter(Q(author__in=subscriptions) | Q(author=user)).order_by('-created_at')
        comments = Comment.objects.all()
        if self.search_value:
            context['accounts'] = self.get_queryset()
        context['posts'] = posts
        context['answer'] = self.answer
        context['form'] = self.form
        context['comment_form'] = CommentForm()
        context['comments'] = comments
        return context