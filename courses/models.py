from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    image = models.ImageField(
        upload_to="users/media/course", verbose_name="Картинка курса", **NULLABLE
    )
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, **NULLABLE, verbose_name="Владелец курса")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="название курса",
        related_name="lessons",
        **NULLABLE
    )
    name = models.CharField(max_length=50, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    image = models.ImageField(
        upload_to="users/media/lesson", verbose_name="Картинка урока", **NULLABLE
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, **NULLABLE, verbose_name="Владелец урока")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "course")