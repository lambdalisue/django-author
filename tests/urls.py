from django.contrib import admin
from django.contrib.auth import login, logout
from django.urls import include, path

admin.autodiscover()

urlpatterns = (
    path('admin/', admin.site.urls),
    path(
        'registration/login/',
        login,
        name='login',
    ),
    path(
        'registration/logout/',
        logout,
        name='logout',
    ),
    path('', include('blog.urls')),
)
