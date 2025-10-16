from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView

from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm, UserLoginForm, UserPasswordResetForm, \
    UserPasswordResetConfirmForm, UserPasswordChangeForm
from .models import Profile
from ..blog.models import Post


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'registration/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль пользователя: {self.object.user.username}'
        context['posts'] = Post.custom.filter(author=self.object.user)
        return context


class ProfileUpdateView(UpdateView):
    """
    Представление для редактирования профиля
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'registration/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                return self.render_to_response(context)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'registration/user_register.html'
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context


class UserLoginView(SuccessMessageMixin, auth_views.LoginView):
    """
    Авторизация на сайте
    """
    form_class = UserLoginForm
    template_name = 'registration/user_login.html'
    next_page = 'home'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'registration/password_reset_form.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserPasswordResetConfirmForm
    template_name = 'registration/password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.user.first_name or self.user.username
        return context


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'registration/change_password.html'
    success_message = 'Пароль успешно изменен'
    success_url = reverse_lazy('profile_detail')