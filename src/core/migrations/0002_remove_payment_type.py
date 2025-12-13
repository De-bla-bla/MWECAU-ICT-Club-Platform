# Generated migration to remove payment announcement type

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='announcement_type',
            field=models.CharField(
                choices=[
                    ('general', 'General'),
                    ('department', 'Department Specific'),
                    ('event', 'Event'),
                    ('urgent', 'Urgent'),
                ],
                default='general',
                max_length=20
            ),
        ),
    ]
