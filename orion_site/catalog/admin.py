from django.contrib import admin

from .models import Apartment, BookingRequest, Contract, Favorite

admin.site.register(Apartment)
admin.site.register(BookingRequest)
admin.site.register(Contract)
admin.site.register(Favorite)
