# Generated by Django 3.0.6 on 2020-08-20 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0007_bruckepage_bruke_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bruckepage',
            name='introduction',
        ),
    ]
