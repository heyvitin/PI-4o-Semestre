from django.contrib import admin
from django.urls import include, path
from cadastro import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cadastro.urls')),
]
