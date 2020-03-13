from datetime import date, timedelta

from django.core.management import BaseCommand

from upload.models import Food


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_ids', nargs='+', type=int)
        #
        # # Named (optional) arguments
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     help='Delete poll instead of closing it',
        # )

    def handle(self, *args, **options):
        date_threshold = date.today() + timedelta(days=3)
        food_qs = Food.objects.filter(expiry_date__lt=date_threshold)

        output = food_qs.values_list('name', 'expiry_date')
        self.stdout.write(str(output))
