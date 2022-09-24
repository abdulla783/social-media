# Generated by Django 4.1.1 on 2022-09-14 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_profile_created_at_profile_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='full_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='postcode',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='relationship',
            field=models.CharField(choices=[('single', 'Single'), ('committed', 'Committed'), ('no interest', 'No Interest'), ('married', 'Married'), ('complicated', 'Complicated')], default='none', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
