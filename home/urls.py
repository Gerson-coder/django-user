from django.urls import path
from django.conf import settings
from  home import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home' ),
    path('signup/',views.signup_user, name= 'signup'),
    path('login/',views.login_user, name= 'login_user'),
    path('logout/', views.logout_user, name = 'logout'),
    path('events/', views.events, name = 'events'),
    path('ranking/', views.ranking, name = 'ranking'),
    path('members_fam/', views.members_fam, name = 'members_fam'),
    path('members_eliminated/', views.members_eliminated, name = 'members_eliminated'),
    path('delete-member/', views.delete_member, name='delete_member'),
    path('autocomplete-nickname/', views.autocomplete_nickname, name='autocomplete_nickname'),
    path('restart/',views.restart_member, name='restart_member'),
    path('dashboard/',views.dashboard,name= 'dashboard')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)