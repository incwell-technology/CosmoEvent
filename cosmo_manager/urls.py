from django.urls import path, include
from cosmo_manager import views as cosmo_manager_views

urlpatterns = [
    path('', cosmo_manager_views.verified_user_view, name='verified-user-view'),
    path('verify', cosmo_manager_views.not_verified_index, name="not-verified-index"),
    path('participate', cosmo_manager_views.participate, name="participate"),
    path('resend-code', cosmo_manager_views.resend_code, name="resend-code")
]

