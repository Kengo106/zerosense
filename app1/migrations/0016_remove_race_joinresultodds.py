# Generated by Django 4.2.1 on 2023-08-02 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_horseplace_race_racecomment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='JoinResultOdds',
        ),
    ]
