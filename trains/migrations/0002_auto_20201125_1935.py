# Generated by Django 3.0.11 on 2020-11-25 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0002_auto_20201125_1929'),
        ('trains', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traintest',
            name='from_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_cityset', to='cities.City', verbose_name='Откуда'),
        ),
    ]
