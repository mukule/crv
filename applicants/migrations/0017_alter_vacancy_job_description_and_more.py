# Generated by Django 4.2.1 on 2023-05-23 11:57

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0016_vacancy_date_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='job_description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='requirements',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
