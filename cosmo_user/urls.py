from django.urls import path, include
from cosmo_user import views as users_views
from cosmo_manager import urls as cosmo_manager_urls

urlpatterns = [
    path('login', users_views.user_login, name='user-login'),
    path('register', users_views.user_register, name='user-register'),
    path('logout', users_views.user_logout, name='user-logout'),
    path('verification', users_views.verification, name="verify-user"),
    path('home/', include(cosmo_manager_urls)),
    path('', users_views.index, name='user-index'),
]
