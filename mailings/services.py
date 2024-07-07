import smtplib

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail

from mailings.models import MailingParameters, Logs


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=60)  # Запуск задачи каждую минуту
    scheduler.start()


def send_mailing():
    time = pytz.timezone(settings.TIME_ZONE)
    current_time = datetime.now(time)

    for mailing in MailingParameters.objects.all():
        if mailing.end_date < current_time and mailing.status == 'is_active':
            mailing.status = ['finished_date']
            mailing.save()

    mailings = (
        MailingParameters.objects.filter(start_date__lte=current_time).filter(status__in=['is_active']).filter(
            next_date__lte=current_time)
    )

    for mailing in mailings:
        recipient_list = [client_.email for client_ in mailing.client.all()]
        server = ''
        status = False
        try:
            server = send_mail(
                subject=mailing.message.title,
                message=mailing.message.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False
            )
            server = str(server)
            status = True
        except smtplib.SMTPException as e:
            server = str(e)
            status = False
        finally:
            log = Logs(status_mailing=status, response=server, date_time_mailing=current_time,
                       mailing_parameters=mailing)
            log.save()

            nex_date = None

            if mailing.interval == 'per_day':
                nex_date = mailing.next_date + timezone.timedelta(days=1)
            elif mailing.interval == 'per_week':
                nex_date = mailing.next_date + timezone.timedelta(weeks=1)
            elif mailing.interval == 'per_month':
                nex_date = mailing.next_date + timezone.timedelta(days=30)

            if nex_date > mailing.end_date:
                if status:
                    mailing.status = 'finished'
                else:
                    mailing.status = 'finished_error'
            else:
                mailing.next_date = nex_date

            mailing.save()
