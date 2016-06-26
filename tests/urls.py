from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = (
    url(r'^admin/', admin.site.urls),
    url(r'^registration/login/$', auth_views.login,
        name='login'),
    url(r'^registration/logout/$', auth_views.logout,
        name='logout'),
    url(r'^', include('blog.urls')),
)
