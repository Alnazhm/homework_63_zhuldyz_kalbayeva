from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from accounts.forms import LoginForm, SearchForm
from accounts.forms import CustomUserCreationForm
from accounts.forms import UserChangeForm
from posts.models import Post
from accounts.models import Account



class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        next = request.GET.get('next')
        form_data = {} if not next else {'next': next}
        form = self.form(form_data)
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            return redirect('login')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        next = form.cleaned_data.get('next')
        account = authenticate(request, email=email, password=password)
        if not account:
            return redirect('login')
        login(request, account)
        if next:
            return redirect(next)
        return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('login')


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            account = form.save()
            login(request, account)
            return redirect('profile', pk=account.pk)
        context = {}
        context['form'] = form
        return self.render_to_response(context)


class ProfileView(DetailView):
    template_name = 'user_detail.html'
    model = Account
    answer = 'accounts'

    def get(self, request, *args, **kwargs):
        self.form = SearchForm(self.request.GET)
        if self.form.is_valid():
            self.search_value = self.form.cleaned_data.get('search')
        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True)
        if self.search_value:
            queryset = Account.objects.filter(Q(username__icontains=self.search_value) |
                                              Q(email__icontains=self.search_value) |
                                              Q(first_name__icontains=self.search_value))
            if len(queryset) == 0:
                self.answer = 'no'
            else:
                self.answer = 'yes'
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.object
        subscriptions = account.subscriptions.count()
        subscribers = account.subscribers.count()
        posts = Post.objects.filter(author=account).order_by('-created_at').exclude(is_deleted=True)
        if self.search_value:
            context['accounts'] = self.get_queryset()
        context['answer'] = self.answer
        context['posts'] = posts
        context['form'] = self.form
        context['subscriptions'] = subscriptions
        context['subscribers'] = subscribers
        return context



class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'


    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        author = Account.objects.get(pk=self.kwargs.get('pk'))
        if request.user != author:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProfileFollowView(TemplateView):
    template_name = 'profile.html'

    def post(self, request, *args, **kwargs):
        from_user = request.user
        to_user = Account.objects.get(id=kwargs['pk'])
        to_user.subscribers.add(from_user)
        return redirect('profile', pk=to_user.pk)


class UserPasswordChangeView(UpdateView):
    model = get_user_model()
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def get(self, request, **kwargs):
        print(self.request.user)
        print(self.object.pk)



    def get_success_url(self):
        return reverse('login')

