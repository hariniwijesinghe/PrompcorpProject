# Generated by Django 4.2.9 on 2024-05-20 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appAdmin', '0024_alter_materialinvoice_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialinvoice',
            name='store_branch_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAdmin.storesbranch'),
        ),
    ]