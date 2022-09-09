from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order
from math import ceil


class CourseInline(admin.TabularInline):
    model = Course


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    inlines = [
        CourseInline,
    ]


class CourseAdmin(admin.ModelAdmin):
    # newly added starts here
    list_display = ('name', 'price')
    actions = ['discount_10']

    def discount_10(self, request, queryset):

        discount = 10  # percentage
        for product in queryset:
            """ Set a discount of 30% to selected products """
            multiplier = discount / 100  # discount / 100 in python 3
            old_price = ceil(product.price)
            new_price = old_price - (old_price * multiplier)
            product.price = new_price
            product.save(update_fields=['price'])

    discount_10.short_description = 'Set 10%% discount'

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','address')

admin.site.register(Topic, TopicAdmin)
#admin.site.register(StudentAdmin)
# admin.site.register(Topic)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Order)
