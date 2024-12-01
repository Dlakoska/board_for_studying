from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=12, verbose_name="Телефон", **NULLABLE)
    city = models.CharField(max_length=30, verbose_name="Город", **NULLABLE)
    image = models.ImageField(
        upload_to="users/media/avatars", **NULLABLE, verbose_name="Аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="payments", **NULLABLE)
    payment_date = models.DateField(verbose_name="Дата оплаты", auto_now_add=True, **NULLABLE)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE)
    separately_paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты", **NULLABLE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты", default="transfer",)
    payment_link = models.URLField(max_length=400, **NULLABLE, verbose_name="Ссылка на оплату",)
    session_id = models.CharField(max_length=255, **NULLABLE, verbose_name="Id сессии",)

    def __str__(self):
        return f"{self.user} - {self.payment_amount} - {self.payment_date}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
