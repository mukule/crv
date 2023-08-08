# Generated by Django 4.2.1 on 2023-07-18 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0032_jobapplication_response'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmailTemplate',
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='job_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='job_ref',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='reports_to',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='vacancytype',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]