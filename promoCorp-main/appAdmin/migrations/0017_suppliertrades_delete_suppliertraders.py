# Generated by Django 4.2.9 on 2024-05-09 04:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appAdmin', '0016_suppliertraders'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierTrades',
            fields=[
                ('worker_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('contact', models.CharField(max_length=128)),
                ('bank_name', models.CharField(max_length=128)),
                ('account_holder_name', models.CharField(max_length=50)),
                ('account_number', models.CharField(max_length=50)),
                ('bsb', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('agent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAdmin.supplier')),
            ],
        ),
        migrations.DeleteModel(
            name='SupplierTraders',
        ),
    ]
