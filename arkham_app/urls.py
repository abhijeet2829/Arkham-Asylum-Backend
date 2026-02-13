from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('security-logs', views.SecurityViewSet, basename='security-logs')
router.register('inmates', views.InmateViewSet, basename='inmates')
router.register('medical-records', views.MedicalViewSet, basename='medical-records')

urlpatterns = [
    path('root/', views.test, name="test"),
    path('default-router/', include(router.urls)),
]