# Generated by Django 3.0.6 on 2020-05-25 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
