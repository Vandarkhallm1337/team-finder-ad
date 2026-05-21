from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)

from .models import Project
from .forms import ProjectForm
from core.mixins import OwnerOrAdminRequiredMixin
from .constants import (
    PAGINATE,
    STATUS_CLOSE_LOWER
)


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = PAGINATE

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
        return reverse(
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
        return reverse(
            'projects:project-detail',
            kwargs={'id': self.object.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_edit'] = True

        return context


@login_required
def toggle_favorite(request, id):
    project = Project.objects.filter(id=id).first()
    if project is None:
        return JsonResponse({'status': 'error',
                             'message': 'Project not found'},
                            status=HTTPStatus.NOT_FOUND)
    favorited = request.user.favorites.filter(id=project.id).exists()
    if favorited:
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)
    return JsonResponse({
        'status': 'ok',
        'favorited': favorited
    })


@login_required
def toggle_participate(request, id):
    project = Project.objects.filter(id=id).first()
    if project is None:
        return JsonResponse({'status': 'error',
                            'message': 'Project not found'},
                            status=HTTPStatus.NOT_FOUND)
    if project.status == STATUS_CLOSE_LOWER:
        return JsonResponse({'status': 'error',
                            'message': 'Project is closed'},
                            status=HTTPStatus.BAD_REQUEST)
    if request.user == project.owner:
        return JsonResponse({'status': 'owner_cannot_join'},
                            status=HTTPStatus.BAD_REQUEST)
    is_participating = project.participants.filter(id=request.user.id).exists()
    if is_participating:
        project.participants.remove(request.user)
        action = 'removed'
    else:
        project.participants.add(request.user)
        action = 'added'
    return JsonResponse({
        'status': 'ok',
        'action': action,
        'participants_count': project.participants.count()
    })


@login_required
def complete_project(request, id):
    project = Project.objects.filter(id=id).first()
    if project is None:
        return JsonResponse({'status': 'error',
                            'message': 'Project not found'},
                            status=HTTPStatus.NOT_FOUND)
    if project.owner != request.user and not request.user.is_staff:
        return JsonResponse({'status': 'error'}, status=HTTPStatus.FORBIDDEN)
    if project.status == STATUS_CLOSE_LOWER:
        return JsonResponse({'status': 'error',
                            'message': 'Project is already closed'},
                            status=HTTPStatus.BAD_REQUEST)
    project.status = STATUS_CLOSE_LOWER
    project.save()

    return JsonResponse({
        'status': 'ok',
        'project_status': STATUS_CLOSE_LOWER
    })
