# Generated by Django 4.0 on 2021-12-25 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naxa_app', '0002_alter_profile_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='interest',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]