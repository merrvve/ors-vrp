# Generated by Django 4.2.9 on 2024-01-27 13:38

from django.db import migrations, models
import django.db.models.deletion
import django_jsonform.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('province', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=20)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='FulfillmentLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_item_id', models.CharField(max_length=255)),
                ('channel_id', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('delivered', models.BooleanField(default=False)),
                ('delivered_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('location', django_jsonform.models.fields.ArrayField(base_field=models.FloatField(), size=2)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('capacity', django_jsonform.models.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('end', django_jsonform.models.fields.ArrayField(base_field=models.FloatField(), default=list, size=2)),
                ('start', django_jsonform.models.fields.ArrayField(base_field=models.FloatField(), default=list, size=2)),
                ('time_window', django_jsonform.models.fields.ArrayField(base_field=models.IntegerField(), default=list, size=2)),
                ('skills', models.ManyToManyField(to='v1.skill')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job_date', models.DateField()),
                ('steps', django_jsonform.models.fields.ArrayField(base_field=django_jsonform.models.fields.ArrayField(base_field=models.FloatField(), size=2), size=None)),
                ('googlelink', models.TextField(default='', max_length=2048)),
                ('vehicle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='v1.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('required_skills', models.ManyToManyField(to='v1.skill')),
            ],
        ),
        migrations.CreateModel(
            name='Fulfillment',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('channel_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('delivered_at', models.DateTimeField()),
                ('display_status', models.CharField(max_length=255)),
                ('in_transit_at', models.DateTimeField()),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('shipment_status', models.CharField(max_length=255)),
                ('total_quantity', models.IntegerField()),
                ('fulfillment_tracking_company', models.CharField(max_length=255)),
                ('fulfillment_tracking_numbers', models.CharField(max_length=255)),
                ('fulfillment_tracking_urls', models.CharField(max_length=255)),
                ('note', models.TextField()),
                ('email_notification', models.BooleanField(default=False)),
                ('sms_notification', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v1.destination')),
                ('fulfillment_line_items', models.ManyToManyField(to='v1.fulfillmentlineitem')),
            ],
        ),
    ]
