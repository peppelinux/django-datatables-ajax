# Generated by Django 3.0 on 2020-01-17 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='edited',
            field=models.DateField(auto_now=True),
        ),
    ]
