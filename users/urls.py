from django.urls import path

from .views import (
    RegisterView,
    LoginWithEmailView,
    UserDetailView,
    ProfileUpdateView,
    UserListView,
    PasswordThreePolesChangeView,
    logout_view
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginWithEmailView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('list/', UserListView.as_view(), name='user-list'),

    path('change-password/', PasswordThreePolesChangeView.as_view(),
         name='change-password'),

    path('<int:id>/', UserDetailView.as_view(), name='user-details'),
    path('edit-profile/', ProfileUpdateView.as_view(), name='edit-profile'),
]
