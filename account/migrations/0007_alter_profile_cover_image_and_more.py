# Generated by Django 4.1.1 on 2022-09-16 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover_image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]