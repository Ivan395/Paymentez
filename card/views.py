import ast
import json
from typing import Any, Optional

from loguru import logger
import requests
from requests import Response as RequestsResponse
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.views import TokenPaymentez
from card.exceptions import SerializerValidationError
from card.serializers import RequestAddCard, ResponseAddCard, RequestGetAllCards, ResponseGetAllCards, \
    RequestDeleteCard, ResponseDeleteCard, RequestRefund, ResponseRefund


def _get_response(token: str, method: str, data_model: Any, serializer: Any, url: str):
    headers = {
        'Content-Type': 'application/json',
        'Auth-Token': token
    }
    response_request: Optional[RequestsResponse] = None
    if method.strip() == 'post':
        response_request: RequestsResponse = requests.post(url=url, data=data_model.data, headers=headers)
    elif method.strip() == 'get':
        response_request: RequestsResponse = requests.get(url=url, data=data_model.data, headers=headers)
    dict_response: dict = ast.literal_eval(response_request.content.decode('UTF-8'))
    response: serializer = serializer(data=dict_response)
    return response


class AddCardView(APIView):
    serializer_class = RequestAddCard
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token: str = TokenPaymentez.get_token_authentication_paymentez()
        response: ResponseAddCard = ResponseAddCard()
        try:
            card_data_request: RequestAddCard = RequestAddCard(data=request.data)
            if card_data_request.is_valid():
                response: ResponseAddCard = _get_response(token, 'post', card_data_request, ResponseAddCard,
                                                          'https://ccapi-stg.paymentez.com/v2/card/add')
                if response.is_valid():
                    return Response(data=response, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as ex:
            st: str = f"{ex}"
            logger.error(st)
            raise serializers.ValidationError(f"Can't serialize data from request client, please contact with the "
                                              f"developer: {ex.__str__()}")
        except Exception as ex:
            st: str = f"{ex}"
            logger.error(st)
            raise SerializerValidationError(f"Error trying serializing data from request client: {ex}")
        return Response(data=response.data, status=status.HTTP_400_BAD_REQUEST)


class GetAllCardsView(APIView):
    serializer_class = RequestGetAllCards
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token: str = TokenPaymentez.get_token_authentication_paymentez()
        response: ResponseGetAllCards = ResponseGetAllCards()
        try:
            all_cards_request: RequestGetAllCards = RequestGetAllCards(data=request.data)
            if all_cards_request.is_valid():
                response: ResponseGetAllCards = _get_response(token, 'get', all_cards_request, ResponseGetAllCards,
                                                              'https://ccapi-stg.paymentez.com/v2/card/list')
                if response.is_valid():
                    return Response(data=response.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as ex:
            logger.error(f"{ex}")
            raise serializers.ValidationError(f"Can't serialize data from request client, please contact with the "
                                              f"developer: {ex}")
        except Exception as ex:
            logger.error(f"{ex}")
            raise SerializerValidationError(f"Error trying serializing data from request client: {ex}")
        return Response(data=response.data, status=status.HTTP_400_BAD_REQUEST)


class DeleteCardView(APIView):
    serializer_class = RequestDeleteCard
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        token: str = TokenPaymentez.get_token_authentication_paymentez()
        response: ResponseDeleteCard = ResponseDeleteCard()
        try:
            delete_card_request: RequestDeleteCard = RequestDeleteCard(data=request.data)
            if delete_card_request.is_valid():
                response: ResponseDeleteCard = _get_response(token, 'post', delete_card_request, ResponseDeleteCard,
                                                             'https://ccapi-stg.paymentez.com/v2/card/delete/')
                if response.is_valid():
                    return Response(data=response.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as ex:
            logger.error(f"{ex}")
            raise serializers.ValidationError(f"Can't serialize data from request client, please contact with the "
                                              f"developer: {ex}")
        except Exception as ex:
            logger.error(f"{ex}")
            raise SerializerValidationError(f"Error trying serializing data from request client: {ex}")
        return Response(data=response.data, status=status.HTTP_400_BAD_REQUEST)


class RefundCard(APIView):
    serializer_class = RequestRefund
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token: str = TokenPaymentez.get_token_authentication_paymentez()
        response: ResponseRefund = ResponseRefund()
        try:
            refund_card_request: RequestRefund = RequestRefund(data=request.data)
            if refund_card_request.is_valid():
                response: ResponseRefund = _get_response(token, 'post', refund_card_request, ResponseRefund,
                                                         'https://ccapi-stg.paymentez.com/v2/transaction/refund/')
                if response.is_valid():
                    return Response(data=response.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as ex:
            logger.error(f"{ex}")
            raise serializers.ValidationError(f"Can't serialize data from request client, please contact with the "
                                              f"developer: {ex}")
        except Exception as ex:
            logger.error(f"{ex}")
            raise SerializerValidationError(f"Error trying serializing data from request client: {ex}")
        return Response(data=response.data, status=status.HTTP_400_BAD_REQUEST)
