# Generated by Django 3.2.15 on 2022-10-02 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dqc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesscount',
            name='AccessCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='accesscount',
            name='Delete_Flg',
            field=models.IntegerField(default=0),
        ),
    ]
