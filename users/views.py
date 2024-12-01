from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
import stripe
from courses.models import Course
from users.filters import PaymentFilter
from users.models import Payment, User
from users.permissions import IsOwner, IsUser
from users.serializers import PaymentSerializer, UserSerializer, UserNotOwnerSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class PaymentViewSet(ModelViewSet):
    """Позволяет автоматически реализовать стандартные методы CRUD для модели Payment"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_stripe_product(payment)
        price = create_stripe_price(payment.payment_amount, product_id)
        session_id, link_payment = create_stripe_session(price)
        payment.session_id = session_id
        payment.payment_link = link_payment
        payment.save()


# class PaymentCreateAPIView(CreateAPIView):
#     """Создать платеж"""
#
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#
#     def perform_create(self, serializer):
#         # Извлекаем course_id из тела url запроса
#         course_id = self.kwargs.get('course_id')
#         # Получаем объект курса по ID
#         course = Course.objects.get(id=course_id)
#         # Сохраняем платеж с указанием пользователя и оплаченного курса
#         payment = serializer.save(user=self.request.user, paid_course=course)
#         try:
#             course_name = course.name
#             session_id, payment_link = create_sessions(payment.payment_amount, f'к оплате {course_name}')
#             payment.session_id = session_id
#             payment.payment_link = payment_link
#             payment.save()
#         except stripe.error.StripeError as e:
#             print(f"Ошибка при создании сессии Stripe: {e}")
#             raise


class UserCreateAPIView(CreateAPIView):
    """Создать пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """Список пользователей"""
    queryset = User.objects.all()
    serializer_class = UserNotOwnerSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """Конкретный пользователь"""
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserSerializer
        # Если пользователь запрашивает свой профиль, используем полный сериализатор
        # if self.request.user == self.get_object():
        #     return UserSerializer
        # else:
        #     return UserNotOwnerSerializer


class UserDestroyAPIView(DestroyAPIView):
    """Удалить пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Изменить пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsUser)


