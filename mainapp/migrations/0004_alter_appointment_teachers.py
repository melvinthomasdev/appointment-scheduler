# Generated by Django 3.2.6 on 2021-08-14 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20210814_0644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='teachers',
            field=models.ManyToManyField(related_name='teachers', to='mainapp.Teacher'),
        ),
    ]
