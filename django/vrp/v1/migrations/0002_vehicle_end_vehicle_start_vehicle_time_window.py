# Generated by Django 4.2.9 on 2024-01-07 14:25

from django.db import migrations, models
import django_jsonform.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='end',
            field=django_jsonform.models.fields.ArrayField(base_field=models.FloatField(), default=[0.0, 0.0], size=2),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='start',
            field=django_jsonform.models.fields.ArrayField(base_field=models.FloatField(), default=[0.0, 0.0], size=2),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='time_window',
            field=django_jsonform.models.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0], size=2),
        ),
    ]