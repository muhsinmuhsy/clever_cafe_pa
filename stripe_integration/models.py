from django.db import models
from auth_manager.models import (
    User
)
class CeUserSubscription(models.Model):
    user = models.OneToOneField(
        User, limit_choices_to={'is_cafe_entrepreneurship_user': True},
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='ce_user'
    )
    price_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    subscription_id = models.CharField(max_length=255, blank=True, null=True)
    subscription_status = models.CharField(max_length=50, blank=True, null=True)
    subscription_start_date = models.DateTimeField(blank=True, null=True)
    subscription_current_period_end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)