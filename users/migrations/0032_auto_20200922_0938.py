# Generated by Django 3.0.6 on 2020-09-22 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_merge_20200911_0434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='providersubscriptionpurchase',
            name='provider',
        ),
        migrations.DeleteModel(
            name='ProviderSubscription',
        ),
        migrations.DeleteModel(
            name='ProviderSubscriptionPurchase',
        ),
    ]
