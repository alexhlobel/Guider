from django.urls import path, include
from .views import GuideViewSet, RegisterView, UserUpdateAPIView, CommentView, GuideLikeView, GuideDislikeView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"guides", GuideViewSet, basename='guides')

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view()),
    path("user-update/", UserUpdateAPIView.as_view()),
    path("comments/<slug:guide_slug>/", CommentView.as_view()),
    path("like/<slug:slug>/", GuideLikeView.as_view()),
    path("dislike/<slug:slug>/", GuideDislikeView.as_view())
]
