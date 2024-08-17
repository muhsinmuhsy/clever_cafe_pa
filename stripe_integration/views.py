import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

stripe.api_key = settings.STRIPE_SECRET_KEY

import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        price_id = settings.CE_PRO_PRICE_ID
        payment_method_id = request.data.get('payment_method_id')
        
        print(f'User ID: {user.username}, Payment Method ID: {payment_method_id}, Price ID: {price_id}')
        
        if not payment_method_id:
            return Response({'error': 'Payment method ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                
                customer_id = user.stripe_customer_id
                
                if not hasattr(request.user, 'stripe_customer_id') or not user.stripe_customer_id:
                    customer = stripe.Customer.create(
                        email=user.email,
                        name=f"{user.profile.first_name} {user.profile.last_name}",
                        payment_method=payment_method_id,
                        invoice_settings={'default_payment_method': payment_method_id}
                    )
                    
                    user.stripe_customer_id = customer.id
                    user.save()

                # Create Stripe subscription
                subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=[{'price': price_id}],
                    expand=['latest_invoice.payment_intent']
                )

            return Response(subscription, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(f'Stripe error: {e}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
# {
#     "payment_method_id":"pm_1PndPoI2SPLgXlZ7VOQul4CQ"
# }

