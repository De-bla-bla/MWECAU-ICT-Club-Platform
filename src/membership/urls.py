from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    path('payment/', views.PaymentListView.as_view(), name='payment_list'),
    path('payment/create/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('payment/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    
    # Webhooks
    path('webhook/mpesa/', views.mpesa_webhook, name='mpesa_webhook'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]
