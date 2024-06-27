from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import URL


class URLSerializer(serializers.ModelSerializer):

    class Meta:
        model = URL
        fields = ['id', 'url', 'status_code', 'last_checked']


class BulkURLSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        user = self.context['request'].user
        urls = [URL(**item, user_id=user) for item in validated_data]
        return URL.objects.bulk_create(urls)

    def update(self, instance, validated_data):
        instance_mapping = {instance_item.id: instance_item for instance_item in instance}
        ret = []
        for item in validated_data:
            instance_item = instance_mapping.get(item['id'], None)
            if instance_item is not None:
                for attr, value in item.items():
                    setattr(instance_item, attr, value)
                instance_item.save()
                ret.append(instance_item)
        return ret


class BulkURLUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = URL
        fields = ['id', 'url', 'status_code', 'last_checked']
        list_serializer_class = BulkURLSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
