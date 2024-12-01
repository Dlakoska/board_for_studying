from rest_framework.fields import SerializerMethodField
from courses.models import Course, Lesson, Subscription
from courses.validators import validate_youtube_link
from rest_framework import serializers


class LessonSerializer(serializers.ModelSerializer):
    # Для уроков добавил валидатор только на ютуб
    video_url = serializers.CharField(validators=[validate_youtube_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = ("id", "name", "lessons", "subscription", "owner")


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'lesson_count', 'lessons')
