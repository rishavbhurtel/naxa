# Generated by Django 4.0 on 2021-12-25 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naxa_app', '0005_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]