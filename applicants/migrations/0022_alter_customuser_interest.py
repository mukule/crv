# Generated by Django 4.2.1 on 2023-05-30 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0021_customuser_interest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='interest',
            field=models.CharField(blank=True, choices=[('I', 'Internship'), ('E', 'Employment')], max_length=255),
        ),
    ]