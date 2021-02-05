from django.utils import timezone

from catalog.models import DataLoad
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Update data of doctors from airtable'

    def handle(self, *args, **options):
        data, new = DataLoad.update_data()
        date = timezone.localtime(data.created_at).strftime('%d-%m-%y  %H:%M:%S')
        if new:
            self.stdout.write(self.style.SUCCESS(f"Success, last update {date}"))
        else:
            self.stdout.write(f"Didn't find the new data. Last update {date}")


