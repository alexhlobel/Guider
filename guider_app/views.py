from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models.query import QuerySet
from .models import Guide, Comment, User
from .serializer import GuideSerializer, RegisterSerializer, UserSerializer, CommentSerializer, AdminGuideSerializer, \
    UserDetailSerializer, GuideLikeSerializer, GuideDislikeSerializer
from .permissions import ComplexGuidePermission
from django.db.models import Q


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


class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request):
        serializer = self.serializer_class(
            get_object_or_404(User, id=request.user.id)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        instance = get_object_or_404(User, id=request.user.id)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GuideViewSet(viewsets.ModelViewSet):
    serializer_class = GuideSerializer
    queryset = Guide.objects.all()
    permission_classes = [ComplexGuidePermission]
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['creator'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            self.queryset = Guide.objects.filter(Q(moderated=True) | Q(creator_id=request.user.id))
        else:
            self.serializer_class = AdminGuideSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_staff:
            self.queryset = Guide.objects.filter(Q(moderated=True) | Q(creator_id=request.user.id))
        else:
            self.serializer_class = AdminGuideSerializer
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.serializer_class = AdminGuideSerializer
            return super().update(request, *args, **kwargs)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['moderated'] = False
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        guide_slug = self.kwargs['guide_slug'].lower()
        guide = Guide.objects.get(slug=guide_slug)
        return Comment.objects.filter(guide=guide)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['author'] = request.user
        serializer.validated_data['guide'] = Guide.objects.get(slug=self.kwargs['guide_slug'].lower())
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GuideRatingView(generics.UpdateAPIView):
    queryset = Guide.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'


class GuideLikeView(GuideRatingView):
    serializer_class = GuideLikeSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        guide = self.get_object()
        serializer = self.get_serializer(guide, data=request.data, partial=partial)

        if guide.likes.filter(id=request.user.id).exists():
            guide.likes.remove(request.user)
        else:
            if guide.dislikes.filter(id=request.user.id).exists():
                guide.dislikes.remove(request.user)
            guide.likes.add(request.user)

        context = {'likes_count': guide.total_likes}

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(guide, '_prefetched_objects_cache', None):
            guide._prefetched_objects_cache = {}

        return Response(serializer.data)


class GuideDislikeView(GuideRatingView):
    serializer_class = GuideDislikeSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        guide = self.get_object()
        serializer = self.get_serializer(guide, data=request.data, partial=partial)

        if guide.dislikes.filter(id=request.user.id).exists():
            guide.dislikes.remove(request.user)
        else:
            if guide.likes.filter(id=request.user.id).exists():
                guide.likes.remove(request.user)
            guide.dislikes.add(request.user)

        context = {'likes_count': guide.total_likes}

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(guide, '_prefetched_objects_cache', None):
            guide._prefetched_objects_cache = {}

        return Response(serializer.data)

# TODO: check images, create rating
