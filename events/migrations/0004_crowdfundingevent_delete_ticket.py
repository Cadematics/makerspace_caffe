# Generated by Django 5.2.2 on 2025-07-01 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrowdfundingEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('goal_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='event_photos/')),
            ],
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
