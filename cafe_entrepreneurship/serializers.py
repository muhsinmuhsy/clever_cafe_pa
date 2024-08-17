from rest_framework import serializers
from .models import (
    AccountHolder, Branch, Event, Image, Review, AdditionalDetail, EcosystemCriteria,
    Declined
)

from food_service.models import (
    Branch as FsBranch
)

from trade_service.models import (
    Branch as TsBranch
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
            'id', 'user', 'account_holder', 'operational_status', 
            'business_name', 'abn', 'email', 'contact_number', 
            'address', 'state', 'location', 'post_code', 
            'weburl', 'instagram', 'facebook', 'linkedin', 
            'twitter', 'tiktok', 'flagship', 'subscription_type', 
            'payment_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'link']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'platform_name', 'review_link']

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
            'saturday_opening_time', 'saturday_closing_time', 'delivery_available', 'delivery_range', 'features',
            'menu_highlights', 'specialist_dietary_services', 'ambiences', 'techstacks', 'images', 'events', 'reviews'
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
        features_ids = validated_data.pop('features', [])
        menu_highlights_ids = validated_data.pop('menu_highlights', [])
        specialist_dietary_services_ids = validated_data.pop('specialist_dietary_services', [])
        ambiences_ids = validated_data.pop('ambiences', [])
        tech_stack_ids = validated_data.pop('techstacks', [])

        additional_detail = AdditionalDetail.objects.create(**validated_data)
        additional_detail.features.set(features_ids)
        additional_detail.menu_highlights.set(menu_highlights_ids)
        additional_detail.specialist_dietary_services.set(specialist_dietary_services_ids)
        additional_detail.ambiences.set(ambiences_ids)
        additional_detail.techstacks.set(tech_stack_ids)

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
        features_ids = validated_data.pop('features', [])
        menu_highlights_ids = validated_data.pop('menu_highlights', [])
        specialist_dietary_services_ids = validated_data.pop('specialist_dietary_services', [])
        ambiences_ids = validated_data.pop('ambiences', [])
        tech_stack_ids = validated_data.pop('techstacks', [])

        # Update AdditionalDetail instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update many-to-many relationships
        instance.features.set(features_ids)
        instance.menu_highlights.set(menu_highlights_ids)
        instance.specialist_dietary_services.set(specialist_dietary_services_ids)
        instance.ambiences.set(ambiences_ids)
        instance.techstacks.set(tech_stack_ids)

        # Update images
        if images_data:
            Image.objects.filter(additional_detail=instance).delete()  # Clear existing images
            for image_data in images_data:
                Image.objects.create(additional_detail=instance, **image_data)

        # Update events
        if events_data:
            Event.objects.filter(additional_detail=instance).delete()  # Clear existing events
            for event_data in events_data:
                Event.objects.create(additional_detail=instance, **event_data)

        # Update reviews
        if reviews_data:
            Review.objects.filter(additional_detail=instance).delete()  # Clear existing reviews
            for review_data in reviews_data:
                Review.objects.create(additional_detail=instance, **review_data)

        return instance

class EcosystemCriteriaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EcosystemCriteria
        fields = [
            'id', 'user', 'branch', 'fs_service_categories',
            'fs_product_types', 'fs_specialist_dietary_services',
            'fs_state', 'ts_service_categories', 'ts_state',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        
# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Like
#         fields = ['user', 'branch', 'created_at', 'updated_at']
#         read_only_fields = ['created_at', 'updated_at']

# class BranchLikeSerializer(serializers.ModelSerializer):
#     likes = serializers.SerializerMethodField()
#     total_likes = serializers.SerializerMethodField()

#     class Meta:
#         model = Branch
#         fields = ['id', 'user', 'created_at', 'updated_at', 'likes', 'total_likes']
#         read_only_fields = ['created_at', 'updated_at']

#     def get_likes(self, obj):
#         return Like.objects.filter(branch=obj).values_list('user', flat=True)

#     def get_total_likes(self, obj):
#         return Like.objects.filter(branch=obj).count()
    
# class DeclinedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Declined
#         fields = ['user', 'branch', 'created_at', 'updated_at']
#         read_only_fields = ['created_at', 'updated_at']
        
class DeclinedFsBranchSerializer(serializers.ModelSerializer):
    declined = serializers.SerializerMethodField()
    
    class Meta:
        model = FsBranch
        fields = ['id', 'user', 'created_at', 'updated_at', 'declined']
        read_only_fields = ['created_at', 'updated_at']

    def get_declined(self, obj):
        return Declined.objects.filter(fs_branch=obj).values_list('user', flat=True)

class DeclinedTsBranchSerializer(serializers.ModelSerializer):
    declined = serializers.SerializerMethodField()
    class Meta:
        model = TsBranch
        fields = ['id', 'user', 'created_at', 'updated_at', 'declined']
        read_only_fields = ['created_at', 'updated_at']

    def get_declined(self, obj):
        return Declined.objects.filter(ts_branch=obj).values_list('user', flat=True)