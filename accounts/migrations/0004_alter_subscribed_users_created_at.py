# Generated by Django 4.1.7 on 2023-02-16 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_patient_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribed_users',
            name='created_at',
            field=models.DateField(auto_now=True),
        ),
    ]
