# Generated by Django 4.2.1 on 2023-05-16 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0003_academiclevel_areaofstudy_course_examiningbody_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialization',
            name='courses',
        ),
    ]