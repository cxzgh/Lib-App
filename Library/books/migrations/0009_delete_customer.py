# Generated by Django 4.0.4 on 2022-10-17 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_customer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]