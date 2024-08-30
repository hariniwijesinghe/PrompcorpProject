# Generated by Django 4.2.9 on 2024-06-03 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appAdmin', '0035_jobordertimesheet_approval_status'),
    ]
    
    operations = [
        migrations.AddField(
            model_name='jobordertimesheet',
            name='work_order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAdmin.workorders'),
            preserve_default=False,
        ),
    ]