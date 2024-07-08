from django.db import models
from django.utils import timezone

from clients.models import Client
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='тема письма', **NULLABLE)
    content = models.TextField(verbose_name='содержание письма', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.content}'

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class MailingParameters(models.Model):
    intervals = (
        ('per_day', 'раз в день'),
        ('per_week', 'раз в неделю'),
        ('per_month', 'раз в месяц')
    )
    status_variants = (
        ('not_active', 'не активна'),
        ('is_active', 'запущена'),
        ('finished', 'закончена успешно'),
        ('finished_date', 'закончена по сроку'),
        ('finished_error', 'законечена с ошибками')
    )
    title = models.CharField(
        max_length=150,
        verbose_name='название рассылки',
        default='mailing_no_name'
    )
    start_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='дата начала рассылки'
    )
    end_date = models.DateTimeField(
        default=(timezone.now() + timezone.timedelta(days=1)),
        verbose_name='дата окончания рассылки'
    )
    next_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='следующая дата рассылки'
    )
    interval = models.CharField(
        max_length=50,
        choices=intervals,
        default='per_day',
        verbose_name='интервал рассылки'
    )
    status = models.CharField(
        max_length=50,
        choices=status_variants,
        default='not_active',
        verbose_name='статус рассылки'
    )
    client = models.ManyToManyField(
        Client, verbose_name='Клиент'
    )
    message = models.ForeignKey(
        Message, verbose_name='Содержание письма',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        User, verbose_name='Создатель',
        on_delete=models.CASCADE,
        **NULLABLE
    )

    def __str__(self):
        return (f'{self.title}: {self.start_date} - {self.end_date};'
                f'интервал: {self.interval};'
                f'статус: {self.status};'
                f'Создатель: {self.owner}')

    class Meta:
        verbose_name = 'параметры рассылки'
        verbose_name_plural = 'параметры рассылок'
        permissions = [
            ('deactivate_mailing', 'Can deactivate mailing'),
            ('view_all_mailings', 'Can view all mailings'),
        ]


class Logs(models.Model):
    mailing_parameters = models.ForeignKey(
        MailingParameters,
        verbose_name='Параметры рассылки',
        on_delete=models.CASCADE
    )
    date_time_mailing = models.DateTimeField(
        auto_now=True,
        verbose_name='дата и время последней рассылке',
        **NULLABLE
    )
    status_mailing = models.CharField(
        max_length=50,
        verbose_name='статус попытки',
        **NULLABLE
    )
    response = models.CharField(
        max_length=255,
        verbose_name='ответ почтового сервера',
        **NULLABLE
    )

    def __str__(self):
        return (f'Параметры сообщения: {self.mailing_parameters},'
                f'Отправлено: {self.date_time_mailing},'
                f'Статус: {self.status_mailing},'
                f'Ответ от постового сервера: {self.response}')

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылок'