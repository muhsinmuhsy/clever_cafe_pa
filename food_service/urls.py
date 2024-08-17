from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    AccountHolderViewSet, AccountHolderWithBranchView, BranchWithAccountHolderView,
    BranchWithIdView, AdditionalDetailWithBranchView, EcosystemCriteriaWithBranchView,
    EcoEcosystemCriteriaCeMatchesView, MediaGalleryForBranchView, BranchViewSet
)

router = DefaultRouter()
router.register(r'account-holders', AccountHolderViewSet, basename='account-holders'),
router.register(r'branches', BranchViewSet, basename='branches')

urlpatterns = [
    path('api/', include(router.urls)),

    # get patch
    path(
        'api/account-holder-with-branch/<int:branch_id>/',
        AccountHolderWithBranchView.as_view(),
        name='account-holder-with-branch-id'
    ),
    
    # post
    path(
        'api/branch-with-account-holder/<int:account_holder_id>/',
        BranchWithAccountHolderView.as_view(),
        name='branch-with-account-holder-id'
    ),
    
    # get patch
    path(
        'api/branch-with-id/<int:branch_id>/',
        BranchWithIdView.as_view(),
        name='branch-with-id'
        ),
    
    # get post patch
    path(
        'api/additional-detail-with-branch-id/<int:branch_id>/',
        AdditionalDetailWithBranchView.as_view(),
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
    
    # get post
    path('api/branch/<int:branch_id>/media-gallery/',
        MediaGalleryForBranchView.as_view(),
        name='media-gallery'),
]
