from rest_framework import serializers
from .models import URL


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ['id', 'user', 'url', 'status_code', 'last_checked']
