from django.conf import settings
from django.db import models


class Apartment(models.Model):
    address = models.CharField('Адрес', max_length=200)
    area = models.PositiveIntegerField('Площадь, кв.м')
    rooms = models.PositiveSmallIntegerField('Количество комнат')
    price = models.PositiveIntegerField('Цена, руб.')
    image = models.ImageField('Фото', upload_to='apartments/', blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'квартира'
        verbose_name_plural = 'квартиры'

    def __str__(self):
        return f'{self.address}, {self.area} кв.м'


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'apartment')
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'


class BookingRequest(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='requests')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField('E-mail клиента')
    created = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self):
        return f'Заявка №{self.pk}'


class Contract(models.Model):
    SIGNING, SIGNED, CANCELLED = 'signing', 'signed', 'cancelled'
    STATUSES = [(SIGNING, 'Подписание'), (SIGNED, 'Подписан'), (CANCELLED, 'Отменён')]

    request = models.OneToOneField(BookingRequest, on_delete=models.CASCADE, related_name='contract')
    employee_code = models.CharField('Код сотрудника', max_length=50)
    signed_date = models.DateField('Дата составления')
    status = models.CharField('Статус', max_length=20, choices=STATUSES, default=SIGNING)
    total_cost = models.PositiveIntegerField('Итоговая стоимость')

    class Meta:
        ordering = ['-id']
        verbose_name = 'договор'
        verbose_name_plural = 'договоры'

    def __str__(self):
        return f'Договор №{self.pk}'

    @property
    def client_name(self):
        client = self.request.client
        return client.get_username() if client else self.request.email
