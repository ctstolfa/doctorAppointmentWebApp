# Generated by Django 4.0.2 on 2022-04-27 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doc_App', '0004_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
