# Generated by Django 3.2.5 on 2021-07-03 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_rename_registercustomer_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='Image',
            field=models.ImageField(default='D:\\Project\\WindsAR\\images\\Passport-smile.jpg', upload_to=None),
        ),
        migrations.AddField(
            model_name='customer',
            name='WinCoins',
            field=models.BigIntegerField(default=0),
        ),
    ]