# Generated by Django 3.0.7 on 2020-07-13 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
    ]
