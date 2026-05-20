from django.urls import path

from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    FavoriteProjectsView,
    toggle_favorite,
    toggle_participate,
    complete_project,
)

app_name = 'projects'

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='project-list'),
    path('favorites/', FavoriteProjectsView.as_view(), name='favorite-projects'),
    path('create-project/', ProjectCreateView.as_view(), name='create-project'),
    path('<int:id>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:id>/edit/', ProjectUpdateView.as_view(), name='edit-project'),
    path('<int:id>/toggle-favorite/', toggle_favorite, name='toggle-favorite'),
    path('<int:id>/toggle-participate/', toggle_participate,
         name='toggle-participate'),
    path('<int:id>/complete/', complete_project, name='complete-project'),
]
