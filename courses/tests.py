from rest_framework.test import APITestCase
from django.shortcuts import reverse
from courses.models import Lesson, Course
from users.models import User
from rest_framework import status


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='dlakoska@test.ru')
        self.course = Course.objects.create(name='Тест1')
        self.lesson = Lesson.objects.create(course=self.course, name="урок для теста1", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('courses:lesson_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse('courses:lesson_create')
        data = {
            'course': '1',
            'name': 'Английский',
            'video_url': 'https://youtube.com/123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('courses:lesson_update', args=(self.lesson.pk,))
        date = {
            'name': 'переименовал'
        }
        response = self.client.patch(url, date)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), 'переименовал'
        )

    def test_lesson_delete(self):
        url = reverse('courses:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест получения списка уроков для курса."""
        url = reverse("courses:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": self.lesson.video_url,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "image": None,
                    "course": self.lesson.course.pk,
                    "owner": self.lesson.owner.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    class SubscriptionTestCase(APITestCase):
        def setUp(self):
            self.user = User.objects.create(email="admin@mail.ru")
            self.course = Course.objects.create(
                name="awgawfawefweaf", description="sefgaesfawe"
            )
            self.client.force_authenticate(user=self.user)

        def test_subscription_post(self):
            """Тест подписки на курс."""
            url = reverse("courses:subscribe_view", args=(self.course.pk,))
            data = {"user": self.user.pk, "course_id": self.course.pk}

            self.assertTrue(Course.objects.filter(pk=self.course.pk).exists())
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.get("message"), "Подписка добавлена")

        def test_unsubscription_post(self):
            """Тест отписки от курса."""

            # Сначала добавляем подписку (если это необходимо)
            url = reverse("courses:subscribe_view", args=(self.course.pk,))
            data = {"user": self.user.pk, "course_id": self.course.pk}
            self.client.post(url, data)  # Добавление подписки

            # Теперь тестируем отписку
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.get("message"), "Подписка удалена")

        def test_subscription_non_existent_course(self):
            """Тест подписки на несуществующий курс."""
            url = reverse("courses:subscribe_view", args=(123123,))
            data = {"user": self.user.pk, "course_id": 123123}
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                response.data.get("detail"),
                "No Course matches the given query.",
            )
