# Generated by Django 5.2.2 on 2025-07-02 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_crowdfundingevent_delete_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='crowdfundingevent',
            name='current_funding',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
