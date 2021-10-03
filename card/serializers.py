from rest_framework import serializers


class ThreeDsTwoData(serializers.Serializer):
    term_url: serializers.CharField(required=True, max_length=50, allow_null=True, allow_blank=True)
    device_type: serializers.CharField(required=True, max_length=7, allow_null=True, allow_blank=True)
    process_anyway: serializers.BooleanField = serializers.BooleanField(required=False, default=False)


class BrowserInfo(serializers.Serializer):
    ip: serializers.IPAddressField = serializers.IPAddressField(required=False, allow_null=True)
    language: serializers.CharField = serializers.CharField(required=False, max_length=50, allow_null=True)
    java_enabled: serializers.BooleanField(required=False, default=False, allow_null=True)
    js_enabled: serializers.BooleanField(required=False, default=False, allow_null=True)
    color_depth: serializers.IntegerField(required=False, allow_null=True)
    screen_height: serializers.IntegerField(required=False, allow_null=True)
    screen_width: serializers.IntegerField(required=False, allow_null=True)
    timezone_offset: serializers.IntegerField(required=False, allow_null=True)
    user_agent: serializers.CharField = serializers.CharField(required=False, max_length=100, allow_null=True)
    accept_header: serializers.CharField = serializers.CharField(required=False, max_length=100, allow_null=True)


class AuthData(serializers.Serializer):
    cavv: serializers.CharField = serializers.CharField(required=True, max_length=100)
    xid: serializers.CharField = serializers.CharField(required=True, max_length=100)
    eci: serializers.CharField = serializers.CharField(required=True, max_length=100)
    version: serializers.CharField = serializers.CharField(required=True, max_length=100)
    reference_id: serializers.UUIDField = serializers.UUIDField(required=True)
    status: serializers.CharField = serializers.CharField(required=True, max_length=100, allow_blank=True)


class ExtraParams(serializers.Serializer):
    threeDS2_data: ThreeDsTwoData = ThreeDsTwoData(required=False, allow_null=True)
    browser_info: BrowserInfo = BrowserInfo(required=False, allow_null=True)
    auth_data: AuthData = AuthData(required=False, allow_null=False)


class BillingAddress(serializers.Serializer):
    street: serializers.CharField = serializers.CharField(required=False, max_length=250, allow_null=True)
    city: serializers.CharField = serializers.CharField(required=False, max_length=50, allow_null=True)
    state: serializers.CharField = serializers.CharField(required=False, max_length=100, allow_null=True)
    district: serializers.CharField = serializers.CharField(required=False, max_length=100, allow_null=True)
    zip: serializers.CharField = serializers.CharField(required=False, max_length=10, allow_null=True)
    house_number: serializers.CharField = serializers.CharField(required=False, max_length=15, allow_null=True)
    country: serializers.CharField = serializers.CharField(required=False, max_length=100, allow_null=True)
    additional_address_info: serializers.CharField = serializers.CharField(required=False, max_length=250, allow_null=True)


class ResponseMessage(serializers.Serializer):
    Mail: serializers.EmailField = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    Result: serializers.CharField = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    Phone: serializers.CharField = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class RequestUser(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(required=True, max_length=100, help_text='user_id is required')
    email: serializers.EmailField = serializers.EmailField(required=True, help_text='email must have a value')
    phone: serializers.CharField = serializers.CharField(required=False, max_length=50, allow_null=True)
    ip_address: serializers.CharField = serializers.CharField(required=False, max_length=50, allow_null=True)
    fiscal_number: serializers.CharField = serializers.CharField(required=False, max_length=50, allow_null=True)


class RequestCard(serializers.Serializer):
    number: serializers.CharField = serializers.CharField(required=True, max_length=16,
                                                          help_text='card number must have a value')
    holder_name: serializers.CharField = serializers.CharField(required=True, max_length=250, allow_null=True)
    expiry_month: serializers.IntegerField = serializers.IntegerField(required=True,
                                                                      help_text='expiration month must have a value')
    expiry_year: serializers.IntegerField = serializers.IntegerField(required=True,
                                                                     help_text='expiration year must have a year')
    cvc: serializers.CharField = serializers.CharField(required=True, max_length=5,
                                                       help_text='cvc number must have a value')
    type: serializers.CharField = serializers.CharField(required=False, max_length=2, allow_null=True)
    nip: serializers.CharField = serializers.CharField(required=False, max_length=6, allow_null=True)
    auth: serializers.CharField = serializers.CharField(required=False, max_length=10, allow_null=True)
    account_type: serializers.CharField = serializers.CharField(required=False, max_length=1, allow_null=True)


class ResponseCard(serializers.Serializer):
    bin: serializers.CharField = serializers.CharField(allow_null=False, allow_blank=True, required=True, max_length=6)
    status: serializers.CharField = serializers.CharField(required=True, max_length=10, allow_blank=True)
    token: serializers.CharField = serializers.CharField(required=True, max_length=50, allow_blank=True)
    message: ResponseMessage = ResponseMessage(required=False, allow_null=True)
    expiry_year: serializers.IntegerField(required=True)
    expiry_month: serializers.IntegerField(required=True)
    transaction_reference: serializers.CharField = serializers.CharField(allow_null=True, required=False, max_length=20)
    type: serializers.CharField = serializers.CharField(required=True, allow_blank=True, max_length=2)
    number: serializers.IntegerField(required=True)
    origin: serializers.CharField = serializers.CharField(required=True, max_length=20, allow_blank=True)


class RequestAddCard(serializers.Serializer):
    session_id: serializers.CharField = serializers.CharField(allow_null=True, allow_blank=True, required=False,
                                                              max_length=32)
    user: RequestUser = RequestUser(required=True)
    card: RequestCard = RequestCard(required=True)
    extra_params: ExtraParams = ExtraParams(required=False, allow_null=True)
    billing_address: BillingAddress = BillingAddress(required=False, allow_null=True)


class ResponseAddCard(serializers.Serializer):
    card: ResponseCard = ResponseCard(required=True)


class ResponseCardAllCards(serializers.Serializer):
    bin: serializers.CharField = serializers.CharField(allow_null=False, allow_blank=True, required=True, max_length=6)
    status: serializers.CharField = serializers.CharField(required=True, max_length=10, allow_blank=True)
    token: serializers.CharField = serializers.CharField(required=True, max_length=50, allow_blank=True)
    holder_name: serializers.CharField = serializers.CharField(required=True, max_length=250, allow_null=True)
    expiry_year: serializers.IntegerField(required=True)
    expiry_month: serializers.IntegerField(required=True)
    transaction_reference: serializers.CharField = serializers.CharField(allow_null=True, required=False, max_length=20)
    type: serializers.CharField = serializers.CharField(required=True, allow_blank=True, max_length=2)
    number: serializers.IntegerField(required=True)


class RequestGetAllCards(serializers.Serializer):
    uid: serializers.CharField = serializers.CharField(required=True, max_length=100, help_text='user_id is required')


class ResponseGetAllCards(serializers.Serializer):
    result_size: serializers.IntegerField = serializers.IntegerField(required=True)
    card: ResponseCardAllCards = ResponseCardAllCards(required=True)


class RequestCardDelete(serializers.Serializer):
    token: serializers.CharField = serializers.CharField(required=True, max_length=50, allow_blank=True,
                                                         help_text='token must have a value')

class RequestUserDelete(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(required=True, max_length=100, help_text='user_id is required')


class RequestDeleteCard(serializers.Serializer):
    card: RequestCardDelete = RequestCardDelete(required=True)
    user: RequestUserDelete = RequestUserDelete(required=True)


class ResponseDeleteCard(serializers.Serializer):
    message: serializers.CharField = serializers.CharField(allow_blank=True, allow_null=True, max_length=250)


class TransactionRefund(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(required=True, max_length=100, help_text='id must have a value')
    reference_label: serializers.CharField = serializers.CharField(required=True, max_length=100,
                                                                   help_text='reference label must have a value')


class OrderRefund(serializers.Serializer):
    amount: serializers.FloatField = serializers.FloatField(required=False)


class RequestRefund(serializers.Serializer):
    transaction: TransactionRefund = TransactionRefund(required=True)
    order: OrderRefund = OrderRefund(required=False)
    more_info: serializers.BooleanField = serializers.BooleanField(required=False, default=False)


class ResponseRefund(serializers.Serializer):
    status: serializers.CharField = serializers.CharField(required=True, max_length=50)
    detail: serializers.CharField = serializers.CharField(required=True, max_length=200)
