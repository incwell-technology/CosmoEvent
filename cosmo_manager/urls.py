from django.urls import path, include
from cosmo_manager import views as cosmo_manager_views

urlpatterns = [
    path('', cosmo_manager_views.verified_user_view, name='verified-user-view'),
    path('verify', cosmo_manager_views.not_verified_index, name="not-verified-index"),
    path('participate', cosmo_manager_views.participate, name="participate"),
    path('resend-code', cosmo_manager_views.resend_code, name="resend-code"),
    path('search', cosmo_manager_views.search, name="search"),
    path('like-video/<int:id>', cosmo_manager_views.like_video, name="like-video"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin', cosmo_manager_views.admin, name="admin"),
    path('admin-users', cosmo_manager_views.admin_users, name="admin-users"),
    path('admin-users-csv', cosmo_manager_views.admin_users_csv, name="admin-users-csv"),
    path('admin-participates', cosmo_manager_views.admin_participates, name="admin-participates"),
    path('admin-participates-csv', cosmo_manager_views.admin_participates_csv, name="admin-participates-csv"),
    path('admin-selected/<int:id>', cosmo_manager_views.admin_selected, name="admin-selected"),
]

