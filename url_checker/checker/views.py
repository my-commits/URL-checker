from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import URL
from .serializers import URLSerializer


class URLViewSet(viewsets.ModelViewSet):
    serializer_class = URLSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return URL.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
