# Generated by Django 3.1.7 on 2021-03-20 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_bill_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date_paid',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Paid On'),
        ),
    ]