
from django.contrib import admin
from .models import Movie, Booking,Transaction

admin.site.register(Movie)
admin.site.register(Booking)
admin.site.register(Transaction)