from django.contrib import admin

from .models import History, Wanted, Category, Soft, Item

admin.site.register(History)
admin.site.register(Wanted)
admin.site.register(Category)
admin.site.register(Soft)
admin.site.register(Item)