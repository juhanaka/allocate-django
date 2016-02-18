from django.contrib import admin
from authentication import models

admin.site.register(models.OutlookCredentialsModel)
admin.site.register(models.RescuetimeTokenModel)
