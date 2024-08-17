from rest_framework import serializers
from .models import (
    AccountHolder, Branch, AdditionalDetail, Image, Event, Review, ServiceCategory,
    EcosystemCriteria, MediaGallery
)

class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHolder
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 
            'contact_number', 'con_num_verify', 'state', 
            'post_code', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        
class BranchSerializer(serializers.ModelSerializer):
    account_holder = AccountHolderSerializer(read_only=True)

    class Meta:
        model = Branch
        fields = [
            'id', 'user', 'account_holder', 
            'business_name', 'abn', 'email', 'contact_number', 
            'address', 'state', 'location', 'post_code', 
            'weburl', 'instagram', 'facebook', 'linkedin', 
            'twitter', 'tiktok', 'headquarter', 
            'payment_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        
class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name']
        read_only_fields = ['created_at', 'updated_at']
        
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'link', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'platform_name', 'review_link', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        
class AdditionalDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    events = EventSerializer(many=True, required=False)
    reviews = ReviewSerializer(many=True, required=False)

    class Meta:
        model = AdditionalDetail
        fields = [
            'id', 'user', 'branch', 'logo', 'menu', 'cover_image',
            'min_bio', 'cafe_registration', 'sunday_availability', 'sunday_opening_time', 'sunday_closing_time',
            'monday_availability', 'monday_opening_time', 'monday_closing_time', 'tuesday_availability',
            'tuesday_opening_time', 'tuesday_closing_time', 'wednesday_availability', 'wednesday_opening_time',
            'wednesday_closing_time', 'thursday_availability', 'thursday_opening_time', 'thursday_closing_time',
            'friday_availability', 'friday_opening_time', 'friday_closing_time', 'saturday_availability',
            'saturday_opening_time', 'saturday_closing_time', 'delivery_available', 'delivery_range', 'service_categories',
            'product_types', 'specialist_dietary_services', 'created_at', 'updated_at', 'images', 'events', 'reviews'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_images(self, obj):
        return ImageSerializer(obj.images.all(), many=True).data

    def get_events(self, obj):
        return EventSerializer(obj.events.all(), many=True).data

    def get_reviews(self, obj):
        return ReviewSerializer(obj.reviews.all(), many=True).data

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        events_data = validated_data.pop('events', [])
        reviews_data = validated_data.pop('reviews', [])
        
        service_categories_ids = validated_data.pop('service_categories', [])
        product_types_ids = validated_data.pop('product_types', [])
        specialist_dietary_services_ids = validated_data.pop('specialist_dietary_services', [])

        additional_detail = AdditionalDetail.objects.create(**validated_data)
        
        additional_detail.service_categories.set(service_categories_ids)
        additional_detail.product_types.set(product_types_ids)
        additional_detail.specialist_dietary_services.set(specialist_dietary_services_ids)

        for image_data in images_data:
            Image.objects.create(additional_detail=additional_detail, **image_data)

        for event_data in events_data:
            Event.objects.create(additional_detail=additional_detail, **event_data)

        for review_data in reviews_data:
            Review.objects.create(additional_detail=additional_detail, **review_data)

        return additional_detail

    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        events_data = validated_data.pop('events', [])
        reviews_data = validated_data.pop('reviews', [])
        service_categories_ids = validated_data.pop('service_categories', [])
        product_types_ids = validated_data.pop('product_types', [])
        specialist_dietary_services_ids = validated_data.pop('specialist_dietary_services', [])
        
        # Update AdditionalDetail instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update many-to-many relationships
        instance.service_categories.set(service_categories_ids)
        instance.product_types.set(product_types_ids)
        instance.specialist_dietary_services.set(specialist_dietary_services_ids)

        # Update images
        if images_data:
            Image.objects.filter(additional_detail=instance).delete() 
            for image_data in images_data:
                Image.objects.create(additional_detail=instance, **image_data)

        # Update events
        if events_data:
            Event.objects.filter(additional_detail=instance).delete()  
            for event_data in events_data:
                Event.objects.create(additional_detail=instance, **event_data)

        # Update reviews
        if reviews_data:
            Review.objects.filter(additional_detail=instance).delete()  
            for review_data in reviews_data:
                Review.objects.create(additional_detail=instance, **review_data)

        return instance


class EcosystemCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcosystemCriteria
        fields = [
            'id', 'user', 'branch', 'ce_operational_status',
            'ce_features', 'ce_specialist_dietary_services',
            'ce_state'
        ]
        read_only_fields = ['id']

class MediaGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaGallery
        fields = ['id', 'user', 'branch', 'file', 'approved', 'uploaded_at']
