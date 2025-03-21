from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'homepage'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), 
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)