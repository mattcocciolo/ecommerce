# Generated by Django 3.1 on 2020-09-25 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_auto_20200924_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]