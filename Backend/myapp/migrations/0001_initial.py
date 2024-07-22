# Generated by Django 5.0.7 on 2024-07-22 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sell_volume', models.DecimalField(decimal_places=2, max_digits=20)),
                ('buy_volume', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sell_orders', models.IntegerField()),
                ('buy_orders', models.IntegerField()),
            ],
        ),
    ]
