# Generated by Django 4.2.9 on 2024-05-02 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appAdmin', '0008_dealcontract_contract_file_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employee_pic',
            field=models.FileField(blank=True, null=True, upload_to='employee/'),
        ),
    ]
