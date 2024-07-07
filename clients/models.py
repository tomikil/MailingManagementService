from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='почта', unique=True)
    last_name = models.CharField(max_length=100, verbose_name='фамилия', **NULLABLE)
    first_name = models.CharField(max_length=100, verbose_name='имя', **NULLABLE)
    patronymic = models.CharField(max_length=100, verbose_name='отчество', **NULLABLE)
    comment = models.CharField(max_length=150, verbose_name='комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)

    def __str__(self):
        return f'{self.email} {self.last_name} {self.first_name} {self.patronymic} {self.comment}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
