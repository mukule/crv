# Generated by Django 4.2.1 on 2023-05-18 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0022_resume_academic_details_resume_employment_history_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='employment_history',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='referee',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='relevant_course',
        ),
        migrations.AddField(
            model_name='resume',
            name='employment_histories',
            field=models.ManyToManyField(blank=True, to='applicants.employmenthistory'),
        ),
        migrations.AddField(
            model_name='resume',
            name='referees',
            field=models.ManyToManyField(blank=True, to='applicants.referee'),
        ),
        migrations.AddField(
            model_name='resume',
            name='relevant_courses',
            field=models.ManyToManyField(blank=True, to='applicants.relevantcourse'),
        ),
        migrations.RemoveField(
            model_name='resume',
            name='academic_details',
        ),
        migrations.AddField(
            model_name='resume',
            name='academic_details',
            field=models.ManyToManyField(blank=True, to='applicants.academicdetails'),
        ),
    ]
