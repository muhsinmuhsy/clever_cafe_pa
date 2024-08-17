from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    AccountHolder, Branch, AdditionalDetail, EcosystemCriteria, MediaGallery
)
from .serializers import (
    AccountHolderSerializer, BranchSerializer, AdditionalDetailSerializer,
    EcosystemCriteriaSerializer, MediaGallerySerializer
)
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError

from cafe_entrepreneurship.models import (
    Branch as CeBranch
)

from cafe_entrepreneurship.serializers import (
    BranchSerializer as CeBranchSerializer
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

class AccountHolderWithBranchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id)
            account_holder = AccountHolder.objects.filter(branch=branch)
            serializer = AccountHolderSerializer(account_holder, many=True)
            return Response(serializer.data)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            account_holder = AccountHolder.objects.get(branch=branch, user=request.user)
        except AccountHolder.DoesNotExist:
            return Response({'error': 'AccountHolder does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountHolderSerializer(account_holder, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(branch=branch)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Exception": f"An error occurred while saving the additional detail: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# {
#     "first_name": "test food",
#     "last_name": "user",
#     "email": "",
#     "contact_number": "",
#     "con_num_verify": false,
#     "state": "",
#     "post_code": ""
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
#     "headquarter": false,
#     "payment_status": false
# }

class BranchWithIdView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id)
            serializer = BranchSerializer(branch)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(branch=branch)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Exception": f"An error occurred while saving the branch: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# {
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
#     "headquarter": false,
#     "payment_status": false
# }

class AdditionalDetailWithBranchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id)
            additional_details = AdditionalDetail.objects.filter(branch=branch)
            serializer = AdditionalDetailSerializer(additional_details, many=True)
            return Response(serializer.data)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, branch_id, format=None):
        try:
            branch = Branch.objects.get(id=branch_id)
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
            branch = Branch.objects.get(id=branch_id)
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
#     "service_categories": [1,2],
#     "product_type": [1,2],
#     "specialist_dietary_services": [1,2],
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
#     "ce_operational_status": "planning",
#     "ce_features": [1, 2],
#     "ce_specialist_dietary_services": [1, 2],
#     "ce_state": [1, 2],
# }


class EcoEcosystemCriteriaCeMatchesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, branch_id):
        try:
            ecosystem_criteria = EcosystemCriteria.objects.get(user=request.user, id=branch_id)
        except EcosystemCriteria.DoesNotExist:
            return Response({'error': 'EcosystemCriteria does not exist or you do not have permission to access it.'}, status=status.HTTP_404_NOT_FOUND)
        
        ce_features = ecosystem_criteria.ce_features.all()
        ce_feature_branches = CeBranch.objects.filter(
            additionaldetail__features__in=ce_features
        )

        ce_specialist_dietary_services = ecosystem_criteria.ce_specialist_dietary_services.all()
        ce_specialist_dietary_service_branches = CeBranch.objects.filter(
            additionaldetail__specialist_dietary_services__in=ce_specialist_dietary_services
        )

        
        ce_states = ecosystem_criteria.ce_state.all()
        ce_state_branches = CeBranch.objects.filter(
            state__in=ce_states
        )

        ce_combined_branches = CeBranch.objects.filter(
            Q(id__in=ce_feature_branches) |
            Q(id__in=ce_specialist_dietary_service_branches) |
            Q(id__in=ce_state_branches) 
        ).distinct()

        # Serialize these branches
        ce_branch_serializer = CeBranchSerializer(ce_combined_branches, many=True)
    
        # Prepare the response
        response_data = {
           "cafe_entrepreneurship": ce_branch_serializer.data
        }
        
        return Response(response_data)
    
class MediaGalleryForBranchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, branch_id=None):
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has access to the branch
        if branch.user != request.user:
            return Response({'warning': 'You do not have access to this branch.'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve media gallery for the branch and user
        media_gallery = MediaGallery.objects.filter(user=request.user, branch=branch)
        if media_gallery.exists():
            serializer = MediaGallerySerializer(media_gallery, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'There is no media gallery in the branch with this user.'}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, branch_id=None):
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        media_gallery = MediaGallery(branch=branch, user=request.user, file=file)
        media_gallery.save()
        serializer = MediaGallerySerializer(media_gallery)
        return Response(serializer.data, status=status.HTTP_201_CREATED)