from django.db import models
from auth_manager.models import User
from common_data.models import State

class AccountHolder(models.Model):
    user = models.ForeignKey(
        User, limit_choices_to={'is_food_service_user': True},
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='fs_accountholder_user'
    )

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True) 
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    con_num_verify = models.BooleanField(default=False)
    state = models.CharField(max_length=50, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name}), ({self.user})"

class Branch(models.Model):
    user = models.ForeignKey(
        User, limit_choices_to={'is_food_service_user': True},
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='fs_branch_user'
    )
    account_holder = models.OneToOneField(AccountHolder,  on_delete=models.SET_NULL, blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    abn = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=555, null=True, blank=True)
    state = models.ForeignKey(State, blank=True, null=True, on_delete=models.SET_NULL, related_name='food_service_branch')
    location = models.CharField(max_length=255, null=True, blank=True)
    post_code = models.CharField(max_length=10, null=True, blank=True)
    weburl = models.CharField(max_length=500, blank=True, null=True)
    instagram = models.CharField(max_length=500, blank=True, null=True)
    facebook = models.CharField(max_length=500, blank=True, null=True)
    linkedin = models.CharField(max_length=500, blank=True, null=True)
    twitter = models.CharField(max_length=500, blank=True, null=True)
    tiktok = models.CharField(max_length=500, blank=True, null=True)
    headquarter = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
class ProductType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
class SpecialistDietaryService(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class AdditionalDetail(models.Model):
    user = models.ForeignKey(
        User, limit_choices_to={'is_food_service_user': True},
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='fs_additional_detail_user'
    )
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    logo = models.ImageField(upload_to='food-service/additional-detail/logo', blank=True, null=True)
    menu = models.ImageField(upload_to='food-service/additional-detail/menu', blank=True, null=True)
    cover_image = models.ImageField(upload_to='food-service/additional-detail/cover', blank=True, null=True)
    min_bio = models.CharField(max_length=555, blank=True, null=True)
    cafe_registration = models.CharField(max_length=250, blank=True, null=True)
    
    sunday_availability = models.BooleanField(default=False)
    sunday_opening_time = models.TimeField(blank=True, null=True)
    sunday_closing_time = models.TimeField(blank=True, null=True)
    monday_availability = models.BooleanField(default=False)
    monday_opening_time = models.TimeField(blank=True, null=True)
    monday_closing_time = models.TimeField(blank=True, null=True)
    tuesday_availability = models.BooleanField(default=False)
    tuesday_opening_time = models.TimeField(blank=True, null=True)
    tuesday_closing_time = models.TimeField(blank=True, null=True)
    wednesday_availability = models.BooleanField(default=False)
    wednesday_opening_time = models.TimeField(blank=True, null=True)
    wednesday_closing_time = models.TimeField(blank=True, null=True)
    thursday_availability = models.BooleanField(default=False)
    thursday_opening_time = models.TimeField(blank=True, null=True)
    thursday_closing_time = models.TimeField(blank=True, null=True)
    friday_availability = models.BooleanField(default=False)
    friday_opening_time = models.TimeField(blank=True, null=True)
    friday_closing_time = models.TimeField(blank=True, null=True)
    saturday_availability = models.BooleanField(default=False)
    saturday_opening_time = models.TimeField(blank=True, null=True)
    saturday_closing_time = models.TimeField(blank=True, null=True)
    
    delivery_available = models.BooleanField(default=False)
    delivery_range = models.PositiveBigIntegerField(blank=True, null=True)
    
    service_categories = models.ManyToManyField(
        ServiceCategory, blank=True,
    )
    product_types = models.ManyToManyField(
        ProductType, blank=True
    )
    specialist_dietary_services = models.ManyToManyField(
        SpecialistDietaryService, blank=True,
    )
    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
class Image(models.Model):
    additional_detail = models.ForeignKey(AdditionalDetail, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='food-service/additionaldetail/images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
class Event(models.Model):
    additional_detail = models.ForeignKey(AdditionalDetail, on_delete=models.CASCADE,  related_name='events', null=True, blank=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    link = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class Review(models.Model):
    additional_detail = models.ForeignKey(AdditionalDetail, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    platform_name = models.CharField(max_length=100, blank=True, null=True)
    review_link = models.CharField(max_length=555, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class EcosystemCriteria(models.Model):
    user = models.ForeignKey(
        User, limit_choices_to={'is_food_service_user': True},
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='fs_ecosystem_criteria_user'
    )
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    
    OPERATIONAL_STATUS_CHOICES = [
        ('planning', 'Planning to open'),
        ('open', 'Open for business'),
        ('exiting', 'Looking to exit'),
    ]
    ce_operational_status = models.CharField(
        max_length=10,
        choices=OPERATIONAL_STATUS_CHOICES,
        null=True, blank=True
    )
    
    ce_features = models.ManyToManyField(
        'cafe_entrepreneurship.Feature', blank=True,
    )
    ce_specialist_dietary_services = models.ManyToManyField(
        'cafe_entrepreneurship.SpecialistDietaryService', blank=True
    )
    ce_state = models.ManyToManyField(
        State, related_name='fs_ecosystem_criteria_state_for_ce'
    )

class MediaGallery(models.Model):
    user = models.ForeignKey(
        User, limit_choices_to={'is_food_service_user': True},
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='fs_media_gallery_user'
    )
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='media-gallery/files/', null=True, blank=True)
    approved = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)