from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    AccountHolder, Branch, AdditionalDetail, EcosystemCriteria,
    Declined
)
from .serializers import (
    AccountHolderSerializer, BranchSerializer, AdditionalDetailSerializer, EcosystemCriteriaSerializer,
    DeclinedFsBranchSerializer, DeclinedTsBranchSerializer
)
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError

from food_service.models import (
    Branch as FsBranch,
)

from food_service.serializers import (
    BranchSerializer as FsBranchSerializer
)

from trade_service.models import (
    Branch as TsBranch
)

from trade_service.serializers import (
    BranchSerializer as TsBranchSerializer
)

from django.db.models import Q

class AccountHolderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountHolderSerializer
    
    def get_queryset(self):
        return AccountHolder.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
# {
#     "first_name": "test food",
#     "last_name": "user",
#     "email": "",
#     "contact_number": "",
#     "con_num_verify": false,
#     "state": "",
#     "post_code": ""
# }

class EditFirstBranchAccountHolderView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, account_holder_id=None, format=None):
        try:
            account_holder = AccountHolder.objects.get(id=account_holder_id, user=request.user)
        except AccountHolder.DoesNotExist:
            return Response({"error": "Account holder not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        branch = Branch.objects.filter(user=user).first()

        if branch is None:
            return Response({"error": "No branch found for the user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BranchSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                branch.account_holder = account_holder
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Exception": f"An error occurred while saving the branch: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# {
#     "operational_status": "open",
#     "business_name": "Updated Business Name",
#     "abn": "98765432101",
#     "email": "updated@example.com",
#     "contact_number": "0123456789",
#     "address": "456 New Address",
#     "state": 1,
#     "location": "Melbourne",
#     "post_code": "3000",
#     "weburl": "http://www.updatedwebsite.com",
#     "instagram": "updated_instagram",
#     "facebook": "updated_facebook",
#     "linkedin": "updated_linkedin",
#     "twitter": "updated_twitter",
#     "tiktok": "updated_tiktok",
#     "flagship": false,
#     "subscription_type": "lite",
#     "payment_status": false
# }

class BranchWithAccountHolderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, account_holder_id, format=None):
        try:
            account_holder = AccountHolder.objects.get(id=account_holder_id, user=request.user)
            branch = Branch.objects.filter(account_holder=account_holder)
            serializer = AccountHolderSerializer(branch, many=True)
            return Response(serializer.data)
        except AccountHolder.DoesNotExist:
            return Response({'error': 'Account holder does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, account_holder_id, format=None):
        try:
            account_holder = AccountHolder.objects.get(id=account_holder_id, user=request.user)
        except AccountHolder.DoesNotExist:
            return Response({'error': 'account holder does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(account_holder=account_holder, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'This account holder already has branch associated with it.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"Exception": f"An error occurred while saving the branch: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, account_holder_id, format=None):
        try:
            account_holder = AccountHolder.objects.get(id=account_holder_id, user=request.user)
        except AccountHolder.DoesNotExist:
            return Response({'error': 'account holder does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            branch = Branch.objects.get(account_holder=account_holder, user=request.user)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(branch=branch)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Exception": f"An error occurred while saving the additional detail: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# {
#     "operational_status": "open",
#     "business_name": "Updated Business Name",
#     "abn": "98765432101",
#     "email": "updated@example.com",
#     "contact_number": "0123456789",
#     "address": "456 New Address",
#     "state": 1,
#     "location": "Melbourne",
#     "post_code": "3000",
#     "weburl": "http://www.updatedwebsite.com",
#     "instagram": "updated_instagram",
#     "facebook": "updated_facebook",
#     "linkedin": "updated_linkedin",
#     "twitter": "updated_twitter",
#     "tiktok": "updated_tiktok",
#     "flagship": false,
#     "subscription_type": "lite",
#     "payment_status": false
# }

    
class AdditionalDetailWithBranchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id, user=request.user)
            additional_details = AdditionalDetail.objects.filter(branch=branch)
            serializer = AdditionalDetailSerializer(additional_details, many=True)
            return Response(serializer.data)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id, user=request.user)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdditionalDetailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(branch=branch, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'This branch already has additional details associated with it.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"Exception": f"An error occurred while saving the additional detail: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id, user=request.user)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            additional_detail = AdditionalDetail.objects.get(branch=branch, user=request.user)
        except AdditionalDetail.DoesNotExist:
            return Response({'error': 'AdditionalDetail does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdditionalDetailSerializer(additional_detail, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(branch=branch)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Exception": f"An error occurred while saving the additional detail: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# {
#     "logo": null,
#     "menu": null,
#     "cover": null,
#     "min_bio": "A short bio",
#     "cafe_registration": "12345",
#     "sunday_availability": true,
#     "sunday_opening_time": "08:00:00",
#     "sunday_closing_time": "20:00:00",
#     "monday_availability": false,
#     "monday_opening_time": null,
#     "monday_closing_time": null,
#     "tuesday_availability": false,
#     "tuesday_opening_time": null,
#     "tuesday_closing_time": null,
#     "wednesday_availability": false,
#     "wednesday_opening_time": null,
#     "wednesday_closing_time": null,
#     "thursday_availability": false,
#     "thursday_opening_time": null,
#     "thursday_closing_time": null,
#     "friday_availability": false,
#     "friday_opening_time": null,
#     "friday_closing_time": null,
#     "saturday_availability": false,
#     "saturday_opening_time": null,
#     "saturday_closing_time": null,
#     "delivery_available": true,
#     "delivery_range": "10-20km",
#     "features": [1,2],
#     "menu_highlights": [1,2],
#     "specialist_dietary_services": [1,2],
#     "ambiences": [1,2],
#     "techstacks": [1,2],
#     "images": [],
#     "events": [{"title": "Event 1", "link": "http://event1.com"}, {"title": "Event 2", "link": "http://event2.com"}],
#     "reviews": [{"platform_name": "Google Reviews", "review_link": "http://review1.com"}]
# }

class EcosystemCriteriaWithBranchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id, user=request.user)
            ecosystem_criteria = EcosystemCriteria.objects.filter(branch=branch)
            serializer = EcosystemCriteriaSerializer(ecosystem_criteria, many=True)
            return Response(serializer.data)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist or you do not have permission to access it.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id, user=request.user)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist or you do not have permission to access it.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EcosystemCriteriaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(branch=branch, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"Exception": f"An error occurred while saving the Ecosystem criteria: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id, user=request.user)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist or you do not have permission to access it.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            ecosystem_criteria = EcosystemCriteria.objects.get(branch=branch)
        except EcosystemCriteria.DoesNotExist:
            return Response({'error': 'EcosystemCriteria does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EcosystemCriteriaSerializer(ecosystem_criteria, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(branch=branch, user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Exception": f"An error occurred while saving the Ecosystem criteria: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# {
#     "fs_service_categories": [1, 2],
#     "fs_product_types": [1, 2],
#     "fs_specialist_dietary_services": [1, 2],
#     "fs_state": [1, 2],
#     "ts_service_categories":[1,2],
#     "ts_state":[1,2]
# }
    
class EcoEcosystemCriteriaFsMatchesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, branch_id):
        try:
            ecosystem_criteria = EcosystemCriteria.objects.get(user=request.user, id=branch_id)
        except EcosystemCriteria.DoesNotExist:
            return Response({'error': 'EcosystemCriteria does not exist or you do not have permission to access it.'}, status=status.HTTP_404_NOT_FOUND)

        # Get user-defined filters from query parameters
        user_filters = {
            'service_categories': request.query_params.getlist('service_categories', []),
            'product_types': request.query_params.getlist('product_types', []),
            'specialist_dietary_services': request.query_params.getlist('specialist_dietary_services', []),
            'states': request.query_params.getlist('states', []),
        }
        print("User filters:", user_filters)  # Debug

        # Get the filterable branches based on ecosystem criteria
        fs_service_categories = ecosystem_criteria.fs_service_categories.all()
        fs_service_category_branches = FsBranch.objects.filter(
            additionaldetail__service_categories__in=fs_service_categories
        )

        fs_product_types = ecosystem_criteria.fs_product_types.all()
        fs_product_type_branches = FsBranch.objects.filter(
            additionaldetail__product_types__in=fs_product_types
        )

        fs_specialist_dietary_services = ecosystem_criteria.fs_specialist_dietary_services.all()
        fs_specialist_dietary_branches = FsBranch.objects.filter(
            additionaldetail__specialist_dietary_services__in=fs_specialist_dietary_services
        )
        
        fs_states = ecosystem_criteria.fs_state.all()
        fs_state_branches = FsBranch.objects.filter(
            state__in=fs_states
        )

        # Apply user-defined filters
        if user_filters['service_categories']:
            fs_service_category_branches = FsBranch.objects.filter(
                additionaldetail__service_categories__in=user_filters['service_categories']
            )
        
        if user_filters['product_types']:
            fs_product_type_branches = FsBranch.objects.filter(
                additionaldetail__product_types__in=user_filters['product_types']
            )
        
        if user_filters['specialist_dietary_services']:
            fs_specialist_dietary_branches = FsBranch.objects.filter(
                additionaldetail__specialist_dietary_services__in=user_filters['specialist_dietary_services']
            )
        
        if user_filters['states']:
            fs_state_branches = FsBranch.objects.filter(
                state__in=user_filters['states']
            )
        
        if user_filters['states']:
            fs_state_branches = FsBranch.objects.filter(
                state__in=user_filters['states']
            )        

        # Combine the branches from all filters using Q objects
        fs_combined_branches = FsBranch.objects.filter(
            Q(id__in=fs_service_category_branches) |
            Q(id__in=fs_product_type_branches) |
            Q(id__in=fs_specialist_dietary_branches) |
            Q(id__in=fs_state_branches)
        ).distinct()
        
        # Handle ordering
        ordering = request.query_params.get('ordering', 'latest')
        if ordering == 'latest':
            fs_combined_branches = fs_combined_branches.order_by('-id')  
        elif ordering == 'oldest':
            fs_combined_branches = fs_combined_branches.order_by('id')

        # Serialize these branches
        fs_branch_serializer = FsBranchSerializer(fs_combined_branches, many=True)
        
        response_data = {
           "food_services": fs_branch_serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
# GET api/ecosystem-criteria/fs/matches/1/?service_categories=1&service_categories=2&states=3&states=4
# api/ecosystem-criteria/fs/matches/1/?ordering=latest
    
class EcoEcosystemCriteriaTsMatchesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, branch_id):
        try:
            ecosystem_criteria = EcosystemCriteria.objects.get(user=request.user, id=branch_id)
        except EcosystemCriteria.DoesNotExist:
            return Response({'error': 'EcosystemCriteria does not exist or you do not have permission to access it.'}, status=status.HTTP_404_NOT_FOUND)
                
        user_filters = {
            'service_categories': request.query_params.getlist('service_categories', []),
            'states': request.query_params.getlist('states', []),
        }
        print("User filters:", user_filters)
        
        ts_service_categories = ecosystem_criteria.ts_service_categories.all()
        ts_service_category_branches = TsBranch.objects.filter(
            additionaldetail__service_categories__in=ts_service_categories
        )
        
        ts_states = ecosystem_criteria.ts_state.all()
        ts_state_branches = TsBranch.objects.filter(
            state__in=ts_states
        )
        
        if user_filters['service_categories']:
            ts_service_category_branches = FsBranch.objects.filter(
                additionaldetail__service_categories__in=user_filters['service_categories']
            )
        
        if user_filters['states']:
            ts_state_branches = FsBranch.objects.filter(
                state__in=user_filters['states']
            )
        
        ts_combined_branches = TsBranch.objects.filter(
            Q(id__in=ts_service_category_branches) |
            Q(id__in=ts_state_branches)
            
        ).distinct()
        
        ordering = request.query_params.get('ordering', 'latest')
        if ordering == 'latest':
            ts_combined_branches = ts_combined_branches.order_by('-id')  
        elif ordering == 'oldest':
            ts_combined_branches = ts_combined_branches.order_by('id')
        
        ts_branch_serializer = TsBranchSerializer(ts_combined_branches, many=True)
        
        # Prepare the response
        response_data = {
           "trade_services": ts_branch_serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
# GET api/ecosystem-criteria/ts/matches/1/?service_categories=1&service_categories=2&states=3&states=4


# class BranchLikeToggleAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, branch_id):
#         branch = Branch.objects.get(id=branch_id)
#         user = request.user

#         like, created = Like.objects.get_or_create(user=user, branch=branch)

#         if not created:
#             like.delete()

#         serializer = BranchLikeSerializer(branch)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeclinedFsBranchToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, fs_branch_id):
        try:
            fs_branch = FsBranch.objects.get(id=fs_branch_id)
        except FsBranch.DoesNotExist:
            return Response({"error": "Fs Branch not found."}, status=status.HTTP_404_NOT_FOUND)
        user = request.user

        declined, created = Declined.objects.get_or_create(user=user, fs_branch=fs_branch)

        if not created:
            declined.delete()

        serializer = DeclinedFsBranchSerializer(fs_branch)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeclinedTsBranchToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ts_branch_id):
        try:
            ts_branch = TsBranch.objects.get(id=ts_branch_id)
        except TsBranch.DoesNotExist:
            return Response({"error": "Ts Branch not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user

        declined, created = Declined.objects.get_or_create(user=user, ts_branch=ts_branch)

        if not created:
            declined.delete()

        serializer = DeclinedTsBranchSerializer(ts_branch)
        return Response(serializer.data, status=status.HTTP_200_OK)