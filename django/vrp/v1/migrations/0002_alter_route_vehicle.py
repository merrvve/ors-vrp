# Generated by Django 4.2.9 on 2024-01-29 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='vehicle',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='v1.vehicle'),
        ),
    ]
