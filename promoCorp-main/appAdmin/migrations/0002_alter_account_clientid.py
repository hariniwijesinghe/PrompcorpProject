# Generated by Django 4.2.9 on 2024-04-29 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appAdmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='clientID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAdmin.clientgroup'),
        ),
    ]
