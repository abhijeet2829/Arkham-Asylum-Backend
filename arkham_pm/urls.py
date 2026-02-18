from django.contrib import admin
from django.urls import include, path, re_path
from djoser.views import UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/users/', UserViewSet.as_view({'post': 'create'})),
    path('api/auth/users/me/', UserViewSet.as_view({'get': 'me', 'patch': 'me'})),
    path('api/auth/users/set_password/', UserViewSet.as_view({'post': 'set_password'})),

    re_path(r'^api/auth/', include('djoser.urls.jwt')),
    
    path('api/v1/', include('arkham_app.urls')),
]