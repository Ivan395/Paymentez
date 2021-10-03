import os
import time
import hashlib
from base64 import b64encode
from typing import List, Dict

from django.contrib.auth.models import User
from loguru import logger
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import RequestUser, ResponseUser
from card.exceptions import SerializerValidationError


class TokenPaymentez:
    _UNIXTIMESTAMP = 0

    @classmethod
    def get_token_authentication_paymentez(cls):
        server_application_code: str = os.environ.get('APPLICATION_CODE')
        server_app_key: str = os.environ.get('UNIQ_TOKEN')
        unix_timestamp: str = str(int(time.time()))
        if cls._UNIXTIMESTAMP - int(unix_timestamp) > 15:
            cls._UNIXTIMESTAMP = int(unix_timestamp)
        else:
            unix_timestamp = str(cls._UNIXTIMESTAMP)
        uniq_token_string: str = server_app_key + unix_timestamp
        uniq_token_hash: str = hashlib.sha256(uniq_token_string.encode('utf-8')).hexdigest()
        auth_token = b64encode(f'{server_application_code};{unix_timestamp};{uniq_token_hash}'.encode())
        return auth_token.decode('utf-8')


class CreateUserView(APIView):
    serializer_class = RequestUser
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        response: ResponseUser = ResponseUser()
        try:
            request_user: RequestUser = RequestUser(data=request.data)
            if request_user.is_valid(raise_exception=True):
                user = User.objects.create_user(
                    username=request_user.data.get('username'),
                    email=request_user.data.get('email'),
                    first_name=request_user.data.get('first_name'),
                    last_name=request_user.data.get('last_name'),
                    is_superuser=request_user.data.get('is_superuser'),
                    is_staff=request_user.data.get('is_staff'),
                    is_active=request_user.data.get('is_active'),
                )
                user.user_permissions.set(request_user.data.get('user_permissions'))
                user.set_password(request_user.data.get('password'))
                user.save()
                response = ResponseUser(instance=request_user.data)
                return Response(data=response.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as ve:
            error: str = f'{ve}'
            response.message = f'{error}'
            logger.error(error)
            raise serializers.ValidationError(f"Can't serialize data from request client, please contact with the "
                                              f"developer: {error}")
        except Exception as ex:
            error: str = f'{ex}'
            response.message = f'{error}'
            logger.error(error)
            raise SerializerValidationError(f"Error trying serializing data from request client: {error}")
        return Response(data=response.data, status=status.HTTP_400_BAD_REQUEST)


class GetAllUsersView(APIView):
    serializer_class = RequestUser
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response: List[Dict] = []
        try:
            data = User.objects.all()
            if data:
                result = data.all()
                for res in result:
                    response.append({
                        'username': res.username,
                        'email': res.email,
                    })
                return Response(data=response, status=status.HTTP_200_OK)
        except serializers.ValidationError as ve:
            error: str = f'{ve}'
            logger.error(error)
            raise serializers.ValidationError(f"Can't serialize data from request client, please contact with the "
                                              f"developer: {error}")
        except Exception as ex:
            error: str = f'{ex}'
            logger.error(error)
            raise SerializerValidationError(f"Error trying serializing data from request client: {error}")
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
