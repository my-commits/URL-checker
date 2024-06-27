from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import URL
from .serializers import URLSerializer, BulkURLUpdateSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer, LoginSerializer


class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super().create(request, *args, **kwargs)

    def perform_bulk_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            partial = kwargs.pop('partial', False)
            instance = self.get_queryset().filter(pk__in=[item['id'] for item in request.data])
            serializer = BulkURLUpdateSerializer(instance, data=request.data, many=True, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_update(serializer)
            return Response(serializer.data)
        else:
            return super().update(request, *args, **kwargs)

    def perform_bulk_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return URL.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
