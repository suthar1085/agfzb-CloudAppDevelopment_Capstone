from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model=CarModel
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields=['make','name','dealer_id','car_type','car_year']
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields=['name','description']
    inlines=[CarModelInline]
# Register models here
admin.site.register(CarModel)
admin.site.register(CarMake)