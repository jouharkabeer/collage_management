# Generated by Django 5.0.1 on 2024-03-22 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumni',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
