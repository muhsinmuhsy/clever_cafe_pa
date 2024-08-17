from django.db import models
from auth_manager.models import User
from common_data.models import State

class AccountHolder(models.Model):
    user = models.ForeignKey(
        User, limit_choices_to={'is_cafe_entrepreneurship_user': True},
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='ce_accountholder_user'
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True) 
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    con_num_verify = models.BooleanField(default=False)
    state = models.CharField(max_length=50, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name}, {self.user}"


class Branch(models.Model):
    user = models.ForeignKey(
        User, limit_choices_to={'is_cafe_entrepreneurship_user': True},
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='ce_branch_user'
    )
    account_holder = models.OneToOneField(AccountHolder,  on_delete=models.SET_NULL, blank=True, null=True)
    OPERATIONAL_STATUS_CHOICES = [
        ('planning', 'Planning to open'),
        ('open', 'Open for business'),
        ('exiting', 'Looking to exit'),
    ]
    operational_status = models.CharField(
        max_length=10,
        choices=OPERATIONAL_STATUS_CHOICES,
        default='planning'
    )
    business_name = models.CharField(max_length=255, blank=True, null=True)
    abn = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=555, null=True, blank=True)
    state = models.ForeignKey(
        State, blank=True, null=True,
        on_delete=models.SET_NULL, related_name='ce_branch_state'
    )
    location = models.CharField(max_length=255, null=True, blank=True)
    post_code = models.CharField(max_length=10, null=True, blank=True)
    weburl = models.CharField(max_length=500, blank=True, null=True)
    instagram = models.CharField(max_length=500, blank=True, null=True)
    facebook = models.CharField(max_length=500, blank=True, null=True)
    linkedin = models.CharField(max_length=500, blank=True, null=True)
    twitter = models.CharField(max_length=500, blank=True, null=True)
    tiktok = models.CharField(max_length=500, blank=True, null=True)
    flagship = models.BooleanField(default=False)
    SUBSCRIPTION_TYPE = [
        ('lite', 'Lite'),
        ('pro', 'Pro'),
    ]
    subscription_type = models.CharField(max_length=4, choices=SUBSCRIPTION_TYPE, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  
    
class Feature(models.Model):
    name = models.CharField(max_length=100)
    
class MenuHighlight(models.Model):
    name = models.CharField(max_length=100)

class SpecialistDietaryService(models.Model):
    name = models.CharField(max_length=100)

class Ambience(models.Model):
    name = models.CharField(max_length=100)

class TechStack(models.Model):
    name = models.CharField(max_length=100)

class AdditionalDetail(models.Model):
    user = models.ForeignKey(
        User, limit_choices_to={'is_cafe_entrepreneurship_user': True},
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='ce_additional_detail_user'
    )
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    logo = models.ImageField(upload_to='cafe-entrepreneurship/additional-detail/logo', blank=True, null=True)
    menu = models.ImageField(upload_to='cafe-entrepreneurship/additional-detail/menu', blank=True, null=True)
    cover_image = models.ImageField(upload_to='cafe-entrepreneurship/additional-detail/cover', blank=True, null=True)
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
    
    features = models.ManyToManyField(
        Feature, blank=True,
    )
    menu_highlights = models.ManyToManyField(
        MenuHighlight, blank=True,
    )
    specialist_dietary_services = models.ManyToManyField(
        SpecialistDietaryService, blank=True,
    )
    ambiences = models.ManyToManyField(
        Ambience, blank=True,
    )
    techstacks = models.ManyToManyField(
        TechStack, blank=True,
    )
    
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True) 
    
class Image(models.Model):
    additional_detail = models.ForeignKey(AdditionalDetail, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='cafe-entrepreneurship/additional-detail/images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True) 

class Event(models.Model):
    additional_detail = models.ForeignKey(AdditionalDetail, on_delete=models.CASCADE,  related_name='events', null=True, blank=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    link = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True) 

class Review(models.Model):
    additional_detail = models.ForeignKey(AdditionalDetail, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    platform_name = models.CharField(max_length=100, blank=True, null=True)
    review_link = models.CharField(max_length=555, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True) 
    

class EcosystemCriteria(models.Model):
    user = models.ForeignKey(
        User, limit_choices_to={'is_cafe_entrepreneurship_user': True},
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='ce_ecosystem_criteria_user'
    )
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    
    fs_service_categories = models.ManyToManyField(
        'food_service.ServiceCategory', blank=True
    )
    fs_product_types = models.ManyToManyField(
        'food_service.ProductType', blank=True
    )
    fs_specialist_dietary_services = models.ManyToManyField(
        'food_service.SpecialistDietaryService', blank=True
    )
    fs_state = models.ManyToManyField(
        State, related_name='ce_ecosystem_criteria_state_for_fd',
        blank=True
    )
    
    ts_service_categories = models.ManyToManyField(
        'trade_service.ServiceCategory', blank=True
    )
    ts_state = models.ManyToManyField(
        State, related_name='ce_ecosystem_criteria_state_for_td',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  

# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='likes')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  

#     class Meta:
#         unique_together = ('user', 'branch')
        

class Declined(models.Model):
    user = models.ForeignKey(
        User, limit_choices_to={'is_cafe_entrepreneurship_user': True},
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='ce_declined_user'
    )
    fs_branch = models.ForeignKey(
        'food_service.Branch', on_delete=models.CASCADE,
        blank=True, null=True, related_name='ce_declined_for_fs'
    )
    ts_branch = models.ForeignKey(
        'trade_service.Branch', on_delete=models.CASCADE,
        blank=True, null=True, related_name='ce_declined_for_ts'
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        unique_together = (('user', 'fs_branch'), ('user', 'ts_branch'))