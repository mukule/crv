# Generated by Django 4.2.1 on 2023-05-16 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0006_remove_examiningbody_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='applicants.specialization'),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='area_of_study',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specializations', to='applicants.areaofstudy'),
        ),
    ]