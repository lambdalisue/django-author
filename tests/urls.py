from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import login, logout

admin.autodiscover()

urlpatterns = (
    url(r'^admin/', admin.site.urls),
    url(
        r'^registration/login/$',
        login,
        name='login',
    ),
    url(
        r'^registration/logout/$',
        logout,
        name='logout',
    ),
    url(r'^', include('blog.urls')),
)
