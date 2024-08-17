from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    AccountHolderViewSet, AccountHolderWithBranchIdView, BranchWithAccountHolderIdView,
    BranchWithIdView, AdditionalDetailWithBranchId, EcosystemCriteriaWithBranchView,
    EcoEcosystemCriteriaCeMatchesView, BranchViewSet
)

router = DefaultRouter()
router.register(r'account-holders', AccountHolderViewSet, basename='account-holders'),
router.register(r'branches', BranchViewSet, basename='branches')

urlpatterns = [
    path('api/', include(router.urls)),

    # get patch
    path(
        'account-holder-with-branch-id/<int:branch_id>/',
        AccountHolderWithBranchIdView.as_view(),
        name='account-holder-with-branch-id'
    ),
    
    # post
    path(
        'branch-with-account-holder-id/<int:account_holder_id>/',
        BranchWithAccountHolderIdView.as_view(),
        name='branch-with-account-holder-id'
    ),
    
    # get patch
    path(
        'branch-with-id/<int:branch_id>/',
        BranchWithIdView.as_view(),
        name='branch-with-id'
        ),
    
    # get post patch
    path(
        'additional-detail-with-branch-id/<int:branch_id>/',
        AdditionalDetailWithBranchId.as_view(),
        name='additional-detail-with-branch-id'
    ),
    
    # get post patch
    path('api/ecosystem-criteria/<int:branch_id>/branch/', 
        EcosystemCriteriaWithBranchView.as_view(), 
        name='ecosystem-criteria-With-branch'
    ),
    
    # get
    path('api/ecosystem-criteria/ce/matches/<int:branch_id>/', 
        EcoEcosystemCriteriaCeMatchesView.as_view(), 
        name='ecosystem-criteria-With-branch'
    ),
    
]
