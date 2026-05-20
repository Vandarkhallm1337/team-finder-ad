from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)
from .models import Project
from .forms import ProjectForm
from core.mixins import OwnerOrAdminRequiredMixin


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):

        return Project.objects.select_related(
            'owner'
        ).prefetch_related(
            'participants',
            'interested_users'
        ).order_by('-created_at')


class FavoriteProjectsView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/favorite_projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return self.request.user.favorites.all()


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'
    pk_url_kwarg = 'id'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'
    raise_exception = True

    def form_valid(self, form):
        project = form.save(commit=False)

        project.owner = self.request.user

        project.save()

        project.participants.add(self.request.user)

        self.object = project

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'projects:project-detail',
            kwargs={'id': self.object.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_edit'] = False

        return context


class ProjectUpdateView(
    LoginRequiredMixin,
    OwnerOrAdminRequiredMixin,
    UpdateView
):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy(
            'projects:project-detail',
            kwargs={'id': self.object.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_edit'] = True

        return context


@login_required
def toggle_favorite(request, id):
    project = get_object_or_404(Project, id=id)

    if project in request.user.favorites.all():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True

    return JsonResponse({
        'status': 'ok',
        'favorited': favorited
    })


@login_required
def toggle_participate(request, id):

    project = get_object_or_404(Project, id=id)

    if project.status == 'closed':
        return JsonResponse({'status': 'error'}, status=400)

    if request.user == project.owner:
        return JsonResponse({'status': 'owner_cannot_join'}, status=400)

    if request.user in project.participants.all():
        project.participants.remove(request.user)
        action = 'removed'
    else:
        project.participants.add(request.user)
        action = 'added'

    return JsonResponse(
        {
            'status': 'ok',
            'action': action,
            'participants_count': project.participants.count()
        }
    )


@login_required
def complete_project(request, id):
    project = get_object_or_404(Project, id=id)

    if (project.owner != request.user and not request.user.is_staff):
        return JsonResponse({'status': 'error'}, status=403)

    if project.status == 'closed':
        return JsonResponse({'status': 'error'}, status=400)

    project.status = 'closed'
    project.save()
    return JsonResponse({
        'status': 'ok',
        'project_status': 'closed'
    })
