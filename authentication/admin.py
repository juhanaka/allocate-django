from django.contrib import admin
from authentication import models
from django.contrib.auth import models as auth_models

admin.site.register(models.OutlookCredentialsModel)
admin.site.register(models.RescuetimeTokenModel)
admin.site.register(auth_models.Permission)
admin.site.register(models.CompanyModel)
