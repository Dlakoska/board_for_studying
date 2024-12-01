from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from courses.models import Course, Lesson, Subscription
from courses.paginators import MyPaginator
from courses.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from users.permissions import IsModer, IsOwner
from rest_framework.response import Response
from courses.tasks import send_info


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = MyPaginator

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """ Этот метод срабатывает, когда пользователь создает новый курс через API."""

        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """ Метод для проверки является ли пользователь(модератором, собственником, просто пользователем),
         и в зависимости от этого разрешаем или нет, те или иные действия"""

        if self.action == "create":
            self.permission_classes = (~IsModer, IsAuthenticated)  # "~" означает не
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)

        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.save()
        send_info.delay(course_id=course.id)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """ Этот метод срабатывает, когда пользователь создает новый урок через API."""

        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MyPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer | IsOwner)


class SubscriptionView(APIView):
    """Класс для проверки подписан ли пользователь на курс или нет"""

    def post(self, request, course_id, *args, **kwargs):
        user = request.user  # Получаем текущего пользователя

        course_item = get_object_or_404(
            Course, id=course_id
        )  # Получаем объект курса или 404

        # Проверяем, есть ли уже подписка
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(
                user=user, course=course_item
            )  # Создаем подписку
            message = "Подписка добавлена"

        return Response({"message": message})
