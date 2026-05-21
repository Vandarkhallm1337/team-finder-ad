from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        RedirectView.as_view(
            pattern_name="projects:project-list", permanent=False
        ),
    ),
    path("users/", include("users.urls")),
    path("projects/", include("projects.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
