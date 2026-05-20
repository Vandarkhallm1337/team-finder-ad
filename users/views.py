from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    UpdateView,
    ListView
)
from django.views.generic.edit import FormView
from .models import User
from .forms import (
    RegisterForm,
    LoginForm,
    ProfileForm,
    PasswordThreePolesChangeForm
)
from core.mixins import SelfOrAdminRequiredMixin


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('projects:project-list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginWithEmailView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('projects:project-list')

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super().form_valid(form)


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'

    pk_url_kwarg = 'id'


class ProfileUpdateView(LoginRequiredMixin,
                        SelfOrAdminRequiredMixin,
                        UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'users:user-details',
            kwargs={'id': self.request.user.id}
        )


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    paginate_by = 12

    def get_queryset(self):
        queryset = User.objects.all().order_by('-last_login')

        filter_type = self.request.GET.get('filter')

        if self.request.user.is_authenticated:
            if filter_type == 'owners-of-favorite-projects':
                favorite_projects = self.request.user.favorites.all()
                queryset = User.objects.filter(
                    owned_projects__in=favorite_projects
                ).distinct()

            elif filter_type == 'owners-of-participating-projects':
                queryset = User.objects.filter(
                    owned_projects__participants=self.request.user
                ).distinct()

            elif filter_type == 'interested-in-my-projects':
                queryset = User.objects.filter(
                    favorites__owner=self.request.user
                ).distinct()

            elif filter_type == 'participants-of-my-projects':
                queryset = User.objects.filter(
                    participated_projects__owner=self.request.user
                ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['active_filter'] = self.request.GET.get('filter')

        return context


class PasswordThreePolesChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    form_class = PasswordThreePolesChangeForm

    def get_success_url(self):
        return reverse_lazy(
            'users:user-details',
            kwargs={'id': self.request.user.id}
        )


def logout_view(request):
    logout(request)
    return redirect('projects:project-list')
