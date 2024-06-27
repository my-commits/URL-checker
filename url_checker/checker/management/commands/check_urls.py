import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from url_checker.checker.models import URL


class Command(BaseCommand):
    help = 'Check the status of URLs'

    def handle(self, *args, **kwargs):
        urls = URL.objects.all()
        for url_obj in urls:
            try:
                response = requests.get(url_obj.url)
                url_obj.status_code = response.status_code
            except requests.exceptions.RequestException:
                url_obj.status_code = None
            url_obj.last_checked = timezone.now()
            url_obj.save()
        self.stdout.write(self.style.SUCCESS('Successfully checked URLs'))
