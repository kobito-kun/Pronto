# Generated by Django 3.1.4 on 2021-04-30 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clean', '0005_auto_20210205_2348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitems',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitems',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='OrderItems',
        ),
    ]