from django.urls import path, include
from cosmo_user import views as users_views


urlpatterns = [
    path('login', users_views.user_login, name='user-login'),
    path('register', users_views.user_register, name='user-register'),
    path('logout', users_views.user_logout, name='user-logout'),
    # path('home/', include(leave_manager_urls)),
    path('', users_views.index, name='user-index'),
]
