# Generated by Django 4.2.1 on 2023-06-19 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0030_rename_certificate_document_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_person_with_disability',
            field=models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=1),
        ),
        migrations.AddField(
            model_name='customuser',
            name='pwd_no',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
