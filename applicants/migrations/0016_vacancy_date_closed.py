# Generated by Django 4.2.1 on 2023-05-23 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0015_remove_vacancy_date_closed_vacancy_document_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='date_closed',
            field=models.DateField(blank=True, null=True),
        ),
    ]
