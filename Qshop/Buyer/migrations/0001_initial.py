# Generated by Django 2.1.8 on 2019-11-04 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuyCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_user', models.CharField(max_length=32)),
                ('goods_name', models.CharField(max_length=32)),
                ('goods_price', models.FloatField()),
                ('goods_picture', models.ImageField(upload_to='buyer/images')),
                ('goods_number', models.IntegerField()),
                ('goods_total', models.FloatField()),
                ('goods_store', models.IntegerField()),
            ],
        ),
    ]
