from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Apartment, BookingRequest, Contract

APARTMENTS = [
    (35, 1, 12000000), (58, 2, 15800000), (72, 3, 21500000), (64, 2, 17300000),
    (95, 3, 26900000), (110, 4, 33000000), (135, 5, 41500000),
]


class Command(BaseCommand):
    help = 'Заполняет базу демо-данными: квартиры, пользователи, заявки и договоры'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='manager').exists():
            User.objects.create_user('manager', 'manager@example.com', 'manager123', is_staff=True)
        if not User.objects.filter(username='resident').exists():
            User.objects.create_user('resident', 'resident@example.com', 'resident123')
        if Apartment.objects.exists():
            self.stdout.write('Квартиры уже есть, пропускаю.')
            return
        img_dir = settings.BASE_DIR / 'static' / 'img'
        apts = []
        for i, (area, rooms, price) in enumerate(APARTMENTS, start=1):
            apt = Apartment.objects.create(address='Шоссе Энтузиастов 10', area=area, rooms=rooms, price=price)
            photo = img_dir / f'apt{i}.jpg'
            if photo.exists():
                with open(photo, 'rb') as fh:
                    apt.image.save(photo.name, File(fh), save=True)
            apts.append(apt)
        resident = User.objects.get(username='resident')
        today = timezone.localdate()
        for n, (apt, days) in enumerate(zip(apts[:4], (75, 40, 12, 12))):
            req = BookingRequest.objects.create(apartment=apt, client=resident if n % 2 == 0 else None,
                                                email='resident@example.com' if n % 2 == 0 else f'guest{n}@example.com')
            Contract.objects.create(request=req, employee_code=f'EMP-{100 + n}', signed_date=today - timedelta(days=days),
                                    status=Contract.SIGNED if n else Contract.SIGNING, total_cost=apt.price)
        BookingRequest.objects.create(apartment=apts[4], email='new.client@example.com')
        self.stdout.write(self.style.SUCCESS(
            'Готово. Сотрудник: manager / manager123. Жилец: resident / resident123.'))
