# Generated by Django 4.2.1 on 2023-09-10 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0025_delete_joinresultodds_delete_odds_delete_raceresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='Odds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tan', models.IntegerField(default=0)),
                ('fuku_1', models.IntegerField(default=0)),
                ('fuku_2', models.IntegerField(default=0)),
                ('fuku_3', models.IntegerField(default=0)),
                ('umaren', models.IntegerField(default=0)),
                ('umatan', models.IntegerField(default=0)),
                ('wide_12', models.IntegerField(default=0)),
                ('wide_13', models.IntegerField(default=0)),
                ('wide_23', models.IntegerField(default=0)),
                ('renfuku_3', models.IntegerField(default=0)),
                ('rentan_3', models.IntegerField(default=0)),
                ('Race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.race')),
            ],
        ),
    ]