# Generated migration to remove payment models

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentWebhookLog',
        ),
        migrations.DeleteModel(
            name='MembershipPayment',
        ),
    ]
