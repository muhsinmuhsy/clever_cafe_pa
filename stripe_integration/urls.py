from django.urls import path
from .views import (
    CreateSubscriptionView
)

urlpatterns = [
    path('api/createsubscription/',
        CreateSubscriptionView.as_view(),
    )
]
