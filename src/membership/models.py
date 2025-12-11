from django.db import models
from django.conf import settings
from django.utils import timezone


class MembershipPayment(models.Model):
    """Payment records for membership fees"""
    PAYMENT_PROVIDERS = [
        ('mpesa', 'M-Pesa'),
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='membership_payments'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=15000.00,
        verbose_name='Amount (TZS)'
    )
    provider = models.CharField(
        max_length=20,
        choices=PAYMENT_PROVIDERS,
        default='mpesa'
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )
    transaction_id = models.CharField(
        max_length=200,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Transaction ID from Provider'
    )
    reference_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Member Reference Code'
    )
    payment_method_details = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional payment method details'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Membership Payment'
        verbose_name_plural = 'Membership Payments'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.amount} TZS ({self.status})"
    
    def mark_as_paid(self):
        """Mark payment as successful"""
        self.status = 'success'
        self.paid_at = timezone.now()
        self.save()
    
    def is_payment_due(self):
        """Check if membership payment is still pending"""
        return self.status == 'pending'


class PaymentWebhookLog(models.Model):
    """Log for payment webhook events (for audit and debugging)"""
    provider = models.CharField(max_length=20)
    event_type = models.CharField(max_length=50)
    raw_data = models.JSONField()
    processed = models.BooleanField(default=False)
    payment = models.ForeignKey(
        MembershipPayment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='webhook_logs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment Webhook Log'
        verbose_name_plural = 'Payment Webhook Logs'
    
    def __str__(self):
        return f"{self.provider} - {self.event_type} ({self.created_at})"
