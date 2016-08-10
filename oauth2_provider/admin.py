from django.contrib import admin

from .models import Grant, AccessToken, RefreshToken, get_application_model

class ApplicationAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    fields = ('name', 'client_id', 'client_secret', 'client_type', 'authorization_grant_type', 'redirect_uris', 'server_ips', 'skip_authorization', 'require_email_verification','display_on_profile','user',)

class RawIDAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)

Application = get_application_model()

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Grant, RawIDAdmin)
admin.site.register(AccessToken, RawIDAdmin)
admin.site.register(RefreshToken, RawIDAdmin)
