from django.urls import path, include
from .views import GuideViewSet, RegisterView, UserUpdateAPIView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"guides", GuideViewSet, basename='guides')

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view()),
    path("user-update/", UserUpdateAPIView.as_view()),
]
