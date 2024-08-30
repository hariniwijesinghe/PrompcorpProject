# Generated by Django 4.2.9 on 2024-05-06 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appAdmin', '0012_timesheet_added_by_timesheet_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierSkill',
            fields=[
                ('skill_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('skill_name', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]