from django.urls import path, include
from cosmo_manager import views as cosmo_manager_views

urlpatterns = [
    path('', cosmo_manager_views.verified_user_view, name='verified-user-view'),
    path('verify', cosmo_manager_views.not_verified_index, name="not-verified-index"),
    path('participate', cosmo_manager_views.participate, name="participate"),
    path('resend-code', cosmo_manager_views.resend_code, name="resend-code"),
    path('search', cosmo_manager_views.search, name="search"),
    path('like-video/<int:id>', cosmo_manager_views.like_video, name="like-video"),
    path('admin/login',cosmo_manager_views.admin_login, name="admin-login"),
    path('admin', cosmo_manager_views.admin, name="admin"),
    path('admin/admin-users', cosmo_manager_views.admin_users, name="admin-users"),
    path('admin/admin-graph', cosmo_manager_views.admin_graph, name="admin-graph"),
    path('admin/admin-users-csv', cosmo_manager_views.admin_users_csv, name="admin-users-csv"),
    path('admin/admin-participates', cosmo_manager_views.admin_participates, name="admin-participates"),
    path('admin/admin-participates-csv', cosmo_manager_views.admin_participates_csv, name="admin-participates-csv"),
    path('admin/admin-selected/<int:id>', cosmo_manager_views.admin_selected, name="admin-selected"),
    path('admin/admin-notSelected/<int:id>', cosmo_manager_views.admin_notSelected, name="admin-notSelected"),
    path('search-participate/<int:id>', cosmo_manager_views.search_participate, name="search-participate"),
    path('stop-participate/<int:id>', cosmo_manager_views.stop_search_participate, name="stop-search-participate"),
    path('privacy-policy', cosmo_manager_views.policy, name="policy"),
    path('search-video', cosmo_manager_views.search_video, name="search-video")
]

