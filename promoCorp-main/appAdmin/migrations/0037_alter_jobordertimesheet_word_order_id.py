# Generated by Django 4.2.9 on 2024-06-03 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appAdmin', '0036_jobordertimesheet_word_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobordertimesheet',
            name='work_order_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appAdmin.workorders'),
        ),
    ]
