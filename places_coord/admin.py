from django.contrib import admin
from places_coord.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass
