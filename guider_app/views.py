from rest_framework import viewsets, filters, pagination
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Guide, Comment, User
from .serializer import GuideSerializer, RegisterSerializer, UserSerializer, \
    CommentSerializer, AdminGuideSerializer, UserDetailSerializer,\
    GuideLikeSerializer, GuideDislikeSerializer
from .permissions import ComplexGuidePermission
from django.db.models import Q


class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        POST method to register a new user. Login, password and correct repeat of a password required.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data,
            "message": "User has been successfully created",
        })


class UserUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request):
        """
        GET method to get user instance, that would be detailed.
        """
        serializer = self.serializer_class(
            get_object_or_404(User, id=request.user.id)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        PATCH method to add info to fields 'email', 'first_name', 'last_name'
        to user, that has been got by GET method.
        """
        instance = get_object_or_404(User, id=request.user.id)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GuideViewSet(viewsets.ModelViewSet):
    """
    PATCH behavior is described in PUT method.
    DELETE is usual, but is allowed only to admin and moderators.
    """
    serializer_class = GuideSerializer
    queryset = Guide.objects.all()
    permission_classes = [ComplexGuidePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'creator__username']
    filterset_fields = ['creator', 'moderated']
    ordering_fields = ['created_at', 'creator', 'title']
    pagination_class = pagination.PageNumberPagination
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        """
        POST method, that allows authorized users to create a guide.
        Admin and moderators (staff) can create moderated guides at once.
        """
        if request.user.is_staff:
            self.serializer_class = AdminGuideSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['creator'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def list(self, request, *args, **kwargs):
        """
        GET method, that returns list of only moderated guides
        for usual authorized and unauthorized users.
        Staff can see moderated and non-moderated guides.
        """
        if not request.user.is_staff:
            self.queryset = Guide.objects.filter(Q(moderated=True) |
                                                 Q(creator_id=request.user.id))
        else:
            self.serializer_class = AdminGuideSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        GET method, that returns one of moderated guides
        for usual authorized and unauthorized users by given slug.
        Staff can see moderated and non-moderated guides.
        """
        if not request.user.is_staff:
            self.queryset = Guide.objects.filter(Q(moderated=True) |
                                                 Q(creator_id=request.user.id))
        else:
            self.serializer_class = AdminGuideSerializer
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        PUT or PATCH method, that lets usual authorized users make corrections to a guide,
        previously got by retrieve method. After corrections a guide requires moderation.
        Staff can make corrections to any guide and moderate it.
        """
        if request.user.is_staff:
            self.serializer_class = AdminGuideSerializer
            return super().update(request, *args, **kwargs)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['moderated'] = False
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CommentPagination(pagination.PageNumberPagination):
    page_size = 15


class CommentView(generics.ListCreateAPIView):
    """
    A View for creating and reading comments under a guide.
    Only authorized users can see and write comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination

    def get_queryset(self):
        """
        Returns a queryset of comments, that belongs to one guide.
        """
        guide_slug = self.kwargs['guide_slug'].lower()
        guide = get_object_or_404(Guide, slug=guide_slug)
        return Comment.objects.filter(guide=guide)

    def create(self, request, *args, **kwargs):
        """
        POST method, that creates a comment under a guide. Only authorized users can write comments.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['author'] = request.user
        guide = Guide.objects.get(slug=self.kwargs['guide_slug'].lower())
        serializer.validated_data['guide'] = guide
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class GuideRatingView(generics.UpdateAPIView):
    queryset = Guide.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'


class GuideLikeView(GuideRatingView):
    """
    A view with only PUT or PATCH method, that allows to rate a guide with a like.
    A user can place either like or dislike.
    """
    serializer_class = GuideLikeSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        guide = self.get_object()
        serializer = self.get_serializer(guide,
                                         data=request.data,
                                         partial=partial)

        if guide.likes.filter(id=request.user.id).exists():
            guide.likes.remove(request.user)
        else:
            if guide.dislikes.filter(id=request.user.id).exists():
                guide.dislikes.remove(request.user)
            guide.likes.add(request.user)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(guide, '_prefetched_objects_cache', None):
            guide._prefetched_objects_cache = {}

        return Response(serializer.data)


class GuideDislikeView(GuideRatingView):
    """
    A view with only PUT or PATCH method, that allows to rate a guide with a dislike.
    A user can place either like or dislike.
    """
    serializer_class = GuideDislikeSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        guide = self.get_object()
        serializer = self.get_serializer(guide,
                                         data=request.data,
                                         partial=partial)

        if guide.dislikes.filter(id=request.user.id).exists():
            guide.dislikes.remove(request.user)
        else:
            if guide.likes.filter(id=request.user.id).exists():
                guide.likes.remove(request.user)
            guide.dislikes.add(request.user)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(guide, '_prefetched_objects_cache', None):
            guide._prefetched_objects_cache = {}

        return Response(serializer.data)
