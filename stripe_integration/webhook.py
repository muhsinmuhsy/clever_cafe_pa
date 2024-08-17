from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from .utils import unix_to_datetime
from .models import CheckoutSessionRecord, User

import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def collect_stripe_webhook(request) -> JsonResponse:
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    signature = request.META.get("HTTP_STRIPE_SIGNATURE")
    
    if not webhook_secret:
        print("Stripe webhook secret not set.")
        return JsonResponse({'status': 'error', 'message': 'Webhook secret not set'}, status=500)

    if not signature:
        print("Stripe signature missing in the request headers.")
        return JsonResponse({'status': 'error', 'message': 'Signature missing'}, status=400)
    
    payload = request.body

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=signature, secret=webhook_secret
        )
    except ValueError as e:
        print(f'ValueError: {str(e)}')
        return JsonResponse({'status': 'error', 'message': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f'SignatureVerificationError: {str(e)}')
        return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=400)

    event_type = event['type']
    data_object = event['data']['object']

    try:
        if event_type == 'checkout.session.completed':
            session_id = data_object['id']
            subscription_id = data_object.get('subscription')
            
            if subscription_id:
                subscription = stripe.Subscription.retrieve(subscription_id)
                start_date = unix_to_datetime(subscription.start_date)
                current_period_end = unix_to_datetime(subscription.current_period_end)
                subscription_status = subscription.status

                CheckoutSessionRecord.objects.filter(
                    stripe_checkout_session_id=session_id
                ).update(
                    stripe_subscription_id=subscription_id,
                    stripe_subscription_status=subscription_status,
                    stripe_subscription_start_date=start_date,
                    stripe_subscription_current_period_end=current_period_end
                )
                
                # record = CheckoutSessionRecord.objects.get(stripe_checkout_session_id=session_id)
                # record.update_user_domain_limit()
                
                record = CheckoutSessionRecord.objects.filter(
                    stripe_checkout_session_id=session_id
                ).first()
                
                if record:
                    record.update_user_domain_limit()
                
                # record = CheckoutSessionRecord.objects.filter(
                #     stripe_checkout_session_id=session_id
                # ).first()
                
                # if record:
                #     record.subscription_id = subscription_id
                #     record.subscription_status = subscription_status
                #     record.subscription_start_date = start_date
                #     record.subscription_current_period_end = current_period_end
                #     record.save()
                #     record.update_user_domain_limit()
                
                # or
                
                # record = CheckoutSessionRecord.objects.get(stripe_checkout_session_id=session_id)
                # record.subscription_id = subscription_id
                # record.subscription_status = subscription_status
                # record.subscription_start_date = start_date
                # record.subscription_current_period_end = current_period_end
                # record.save()
                # record.update_user_domain_limit()
            
        elif event_type == 'customer.subscription.deleted':
            subscription_id = data_object['id']
            subscription_status = data_object['status']
            CheckoutSessionRecord.objects.filter(
                stripe_subscription_id=subscription_id
            ).update(
                stripe_subscription_status=subscription_status
            )
            
            record = CheckoutSessionRecord.objects.filter(
                    stripe_subscription_id=subscription_id
                ).first()
                
            if record:
                record.update_user_domain_limit()
        
        elif event_type == 'customer.subscription.updated':
            subscription_id = data_object.get('id')
            
            if subscription_id:
                updated_subscription = stripe.Subscription.retrieve(subscription_id)
                start_date = unix_to_datetime(updated_subscription.start_date)
                current_period_end = unix_to_datetime(updated_subscription.current_period_end)
                
                price_id = data_object['items']['data'][0]['price']['id']
                logger.info(price_id)
                print(price_id)
                
                product_id = data_object['items']['data'][0]['price']['product']
                
                logger.info(product_id)
                print(product_id)         
                
                try:
                    product = stripe.Product.retrieve(product_id)
                except Exception as e:
                    logger.error(f'product: {str(e)}')
                
                product_name = product.name
                
                CheckoutSessionRecord.objects.filter(
                    stripe_subscription_id=subscription_id
                ).update(
                    stripe_subscription_status=updated_subscription.status,
                    stripe_subscription_start_date=start_date,
                    stripe_subscription_current_period_end=current_period_end,
                    stripe_price_id=price_id,
                    stripe_product_id=product_id,
                    stripe_product_name=product_name
                )
            
                record = CheckoutSessionRecord.objects.filter(
                        stripe_subscription_id=subscription_id
                    ).first()
                    
                if record:
                    record.update_user_domain_limit()
        
        elif event_type == 'invoice.payment_failed':
            subscription_id = data_object.get('subscription')
            
            if subscription_id:
                subscription = stripe.Subscription.retrieve(subscription_id)
                subscription_status = subscription.status
                CheckoutSessionRecord.objects.filter(
                    stripe_subscription_id=subscription_id
                ).update(
                    stripe_subscription_status=subscription_status
                )
                
                record = CheckoutSessionRecord.objects.filter(
                    stripe_subscription_id=subscription_id
                ).first()
                
                if record:
                    record.update_user_domain_limit()
        
        elif event_type == 'invoice.payment_succeeded':
            subscription_id = data_object.get('subscription')
            
            if subscription_id:
                subscription = stripe.Subscription.retrieve(subscription_id)
                subscription_status = subscription.status
                CheckoutSessionRecord.objects.filter(
                    stripe_subscription_id=subscription_id
                ).update(
                    stripe_subscription_status=subscription_status
                )
                
                record = CheckoutSessionRecord.objects.filter(
                    stripe_subscription_id=subscription_id
                ).first()
                
            if record:
                record.update_user_domain_limit()
        
        elif event_type == 'product.updated':
            product_id = data_object['id']
            product_name = data_object['name']
            metadata = data_object['metadata']

            CheckoutSessionRecord.objects.filter(
                stripe_product_id=product_id
            ).update(
                stripe_product_name=product_name,
                stripe_metadata=metadata
            )
            
        elif event['type'] == 'customer.deleted':
            stripe_customer_id = event['data']['object']['id']
            
            # user = User.objects.get(stripe_customer_id=stripe_customer_id)
            # user.stripe_customer_id = None
            # user.save()
            
            User.objects.filter(stripe_customer_id=stripe_customer_id).update(
                stripe_customer_id=None,
                max_domains=10
            )
            
            
    except Exception as e:
        print(f'Error processing event: {str(e)}')
        return JsonResponse({'status': 'error', 'message': 'Internal Server Error'}, status=500)

    return JsonResponse({'status': 'success'})



# @csrf_exempt
# def collect_stripe_webhook(request) -> JsonResponse:

#     webhook_secret = settings.STRIPE_WEBHOOK_SECRET

#     signature = request.META.get("HTTP_STRIPE_SIGNATURE")
    
#     if not webhook_secret:
#         print("Stripe webhook secret not set.")
#         return JsonResponse({'status': 'error', 'message': 'Webhook secret not set'}, status=500)

#     if not signature:
#         print("Stripe signature missing in the request headers.")
#         return JsonResponse({'status': 'error', 'message': 'Signature missing'}, status=400)
    
#     payload = request.body

#     try:
#         event = stripe.Webhook.construct_event(
#             payload=payload, sig_header=signature, secret=webhook_secret
#         )
#     except ValueError as e:  
#         print(str(e))
#         return JsonResponse({'status': 'error', 'message': 'Invalid payload'}, status=400)
#     except stripe.error.SignatureVerificationError as e:
#         print(f'error: {str(e)}')  
#         return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=400)

#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         session_id = session['id']
#         subscription_id = session.get('subscription')
        
#         if subscription_id:
#             subscription = stripe.Subscription.retrieve(subscription_id)
            
#             start_date = unix_to_datetime(subscription.start_date)
#             current_period_end = unix_to_datetime(subscription.current_period_end)
#             subscription_status = subscription.status

#         try:
            
#             CheckoutSessionRecord.objects.filter(
#                 stripe_checkout_session_id=session_id
#             ).update(
#                 subscription_id=subscription_id,
#                 subscription_status = subscription_status,
#                 subscription_start_date=start_date,
#                 subscription_current_period_end=current_period_end
#             )
#         except Exception as e:
#             print(f'error subscription create: {str(e)}')
        
#     elif event['type'] == 'customer.subscription.deleted':
#         subscription = event['data']['object']
#         status = subscription['status']
#         print(status)
#         CheckoutSessionRecord.objects.filter(
#             subscription_id=subscription['id']
#         ).update(
#             subscription_status=subscription['status']
#         )
        
#     elif event['type'] == 'customer.subscription.updated':
#         subscription = event['data']['object']
#         subscription_id = subscription.get('id')
        
#         if subscription_id:
#             updated_subscription = stripe.Subscription.retrieve(subscription_id)
#             start_date = unix_to_datetime(updated_subscription.start_date)
#             current_period_end = unix_to_datetime(updated_subscription.current_period_end)
            
#             print(updated_subscription.status)
#             CheckoutSessionRecord.objects.filter(
#                 subscription_id=subscription_id
#             ).update(
#                 subscription_status=updated_subscription.status,
#                 subscription_start_date=start_date,
#                 subscription_current_period_end=current_period_end,
#             )
            
#         elif event['type'] == 'invoice.payment_failed':
#             invoice = event['data']['object']
            
#             subscription_id = invoice.get('subscription')
            
#             if subscription_id:
#                 subscription = stripe.Subscription.retrieve(subscription_id)
#                 subscription_status = subscription.status
#                 CheckoutSessionRecord.objects.filter(
#                     subscription_id=subscription_id
#                 ).update(
#                     subscription_status=subscription_status
#                 )

#         elif event['type'] == 'invoice.payment_succeeded':
#             invoice = event['data']['object']
#             subscription_id = invoice.get('subscription')
            
#             if subscription_id:
#                 subscription = stripe.Subscription.retrieve(subscription_id)
#                 subscription_status = subscription.status
#                 CheckoutSessionRecord.objects.filter(
#                     subscription_id=subscription_id
#                 ).update(
#                     subscription_status=subscription_status
#                 )

#     return JsonResponse({'status': 'success'})