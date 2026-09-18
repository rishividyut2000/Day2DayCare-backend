from django.contrib import admin

from .models import Client, Domain


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("display_name", "code", "schema_name", "is_active", "created_at")
    search_fields = ("display_name", "code", "schema_name")


admin.site.register(Domain)
