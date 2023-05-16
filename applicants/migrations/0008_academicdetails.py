# Generated by Django 4.2.1 on 2023-05-16 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0007_course_specialization_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution_name', models.CharField(max_length=100)),
                ('admission_number', models.CharField(max_length=20)),
                ('start_year', models.PositiveIntegerField()),
                ('end_year', models.PositiveIntegerField()),
                ('graduation_year', models.PositiveIntegerField()),
                ('academic_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='applicants.academiclevel')),
                ('area_of_study', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='applicants.areaofstudy')),
                ('examining_body', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='applicants.examiningbody')),
                ('specialization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='applicants.specialization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]