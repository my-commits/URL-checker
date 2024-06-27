from celery import shared_task
import requests
from datetime import datetime
from .models import URL


@shared_task
def update_urls_status():
    urls = URL.objects.all()

    for url in urls:
        try:
            response = requests.get(url.url)
            url.status_code = response.status_code
            url.last_checked = datetime.now()
            url.save()
            print(f'Successfully updated URL: {url.url}')
        except requests.RequestException as e:
            print(f'Failed to update URL: {url.url}. Error: {str(e)}')
