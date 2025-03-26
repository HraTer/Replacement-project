from django.contrib import admin

from replacement.models import Hardware


# Register your models here.
@admin.register(Hardware)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "hw_name", "hw_price", "write_off_length")
    # umozni fulltextove vyhledavani v polich
    search_fields = ("brand_name__brand_name","hw_name", "hw_price")

