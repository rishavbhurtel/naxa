# Generated by Django 4.0 on 2021-12-25 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naxa_app', '0003_alter_profile_bio_alter_profile_birth_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(null=True),
        ),
    ]
