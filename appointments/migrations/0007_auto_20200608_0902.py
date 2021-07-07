# Generated by Django 3.0.6 on 2020-06-08 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0006_merge_20200605_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providerappointment',
            name='status',
            field=models.CharField(choices=[('requested', 'Requested By Client'), ('approved', 'Approved By Provider'), ('canceled', 'Canceled By Provider'), ('completed', 'Appointment Completed')], default='requested', max_length=20),
        ),
    ]
