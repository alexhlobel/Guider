from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import Guide, Comment
from .serializer import GuideSerializer, RegisterSerializer, UserSerializer, CommentSerializer
from .permissions import IsAdminUserOrReadOnly


class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User has been successfully created",
        })


class GuideView(viewsets.ModelViewSet):
    serializer_class = GuideSerializer
    queryset = Guide.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]

    def list(self, request, *args, **kwargs):
        if not request.user.is_stuff:
            self.queryset = Guide.objects.filter(moderated=True)
        queryset = self.filter_queryset(self.get_queryset())
        Guide.objects.filter(moderated=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
