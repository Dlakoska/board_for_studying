from rest_framework.serializers import ModelSerializer
from users.models import Payment, User


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class UserNotOwnerSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "date_joined", "id")

