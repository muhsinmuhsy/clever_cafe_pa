from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    AccountHolderViewSet, EditFirstBranchAccountHolderView, BranchWithAccountHolderView, AdditionalDetailWithBranchView,
    EcosystemCriteriaWithBranchView, EcoEcosystemCriteriaFsMatchesView, EcoEcosystemCriteriaTsMatchesView,
    DeclinedFsBranchToggleView, DeclinedTsBranchToggleView, BranchViewSet
)

router = DefaultRouter()
router.register(r'account-holders', AccountHolderViewSet, basename='account-holders'),
router.register(r'branches', BranchViewSet, basename='branches')

urlpatterns = [
    path('api/', include(router.urls)),
    
    # patch
    path('api/edit-first-branch-with-account-holder/<int:account_holder_id>/', 
        EditFirstBranchAccountHolderView.as_view(), 
        name='edit-first-branch-with-account-holder'
    ),
    
    # get post patch
    path('api/branch/<int:account_holder_id>/account-holder/', 
        BranchWithAccountHolderView.as_view(), 
        name='additional-detail-With-branch'
    ),

    # get post patch
    path('api/additional-detail/<int:branch_id>/branch/', 
        AdditionalDetailWithBranchView.as_view(), 
        name='additional-detail-With-branch'
    ),
    
    # get post patch
    path('api/ecosystem-criteria/<int:branch_id>/branch/', 
        EcosystemCriteriaWithBranchView.as_view(), 
        name='ecosystem-criteria-With-branch'
    ),
    
    # get
    path('api/ecosystem-criteria/fs/matches/<int:branch_id>/', 
        EcoEcosystemCriteriaFsMatchesView.as_view(), 
        name='ecosystem-criteria-With-branch'
    ),
    
    # get
    path('api/ecosystem-criteria/ts/matches/<int:branch_id>/', 
        EcoEcosystemCriteriaTsMatchesView.as_view(), 
        name='ecosystem-criteria-With-branch'
    ),
    
    # post
    path('api/decline/fs-branch/<int:fs_branch_id>/',
        DeclinedFsBranchToggleView.as_view(),
        name='decline_fs_branch_toggle'
    ),
    
    # post
    path('api/decline/ts-branch/<int:ts_branch_id>/',
        DeclinedTsBranchToggleView.as_view(),
        name='decline_ts_branch_toggle'
    ),
]
