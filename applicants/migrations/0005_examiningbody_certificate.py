# Generated by Django 4.2.1 on 2023-05-16 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0004_remove_specialization_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='examiningbody',
            name='certificate',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
