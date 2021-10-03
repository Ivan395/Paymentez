from django.contrib.auth.models import User
from rest_framework import serializers


class RequestUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ResponseUser(serializers.Serializer):
    email: serializers.EmailField = serializers.EmailField(max_length=150)
    username: serializers.CharField = serializers.CharField(max_length=150, allow_null=True, allow_blank=True)
    message: serializers.CharField = serializers.CharField(required=False, max_length=150, allow_null=True,
                                                           allow_blank=True)
