from django.db import models

from config import settings
from users.models import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='course_previews/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ('title', )


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='превью', **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='курс')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ('course', 'title', )


class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата оплаты', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='payments', **NULLABLE)
    payment_sum =
    payment_type =

    def __str__(self):
        return f"{self.user} - {self.payment_date}"

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ('payment_date', 'user')
