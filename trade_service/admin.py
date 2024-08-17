from django.contrib import admin
from .models import (
    AccountHolder, Branch, AdditionalDetail, ServiceCategory,
    Image, Event, Review, EcosystemCriteria, MediaGallery
)

admin.site.register(AccountHolder)
admin.site.register(Branch)
admin.site.register(AdditionalDetail)
admin.site.register(ServiceCategory)
admin.site.register(Image)
admin.site.register(Event)
admin.site.register(Review)
admin.site.register(EcosystemCriteria)
admin.site.register(MediaGallery)
