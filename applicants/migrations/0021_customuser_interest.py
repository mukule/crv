# Generated by Django 4.2.1 on 2023-05-30 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0020_academicdetails_is_studying_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='interest',
            field=models.CharField(blank=True, choices=[('I', 'Internship'), ('E', 'Employment')], max_length=1),
        ),
    ]
