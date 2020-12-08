from django.contrib import admin
from .models import Route
# admin.site.register(Route)


class RouteAdmin(admin.ModelAdmin):
    class Meta:
        model = Route
    # fields = ('name', 'from_city', 'to_city', 'travel_times')
    list_display = ('name', 'from_city', 'to_city', 'travel_times')
    list_editable = ['from_city']


admin.site.register(Route, RouteAdmin)
