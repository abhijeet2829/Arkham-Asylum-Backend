from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),

# Authentication (JWT)
    re_path(r'^api/auth/', include('djoser.urls')),
    re_path(r'^api/auth/', include('djoser.urls.jwt')),
    
    path('api/v1/', include('arkham_app.urls')),
]