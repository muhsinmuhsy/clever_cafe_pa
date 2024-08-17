from django.contrib import admin
from .models import (
    AccountHolder, Branch, Feature, MenuHighlight, SpecialistDietaryService, Ambience, TechStack, AdditionalDetail,
    Image, Event, Review, EcosystemCriteria, Declined
)

admin.site.register(AccountHolder)
admin.site.register(Branch)
admin.site.register(Feature)
admin.site.register(MenuHighlight)
admin.site.register(SpecialistDietaryService)
admin.site.register(Ambience)
admin.site.register(TechStack)
admin.site.register(AdditionalDetail)
admin.site.register(Image)
admin.site.register(Event)
admin.site.register(Review)
admin.site.register(EcosystemCriteria)
admin.site.register(Declined)