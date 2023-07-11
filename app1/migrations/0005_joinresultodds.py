# Generated by Django 4.2.1 on 2023-07-06 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_remove_odds_unique_odds_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinResultOdds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horse_name', models.CharField(max_length=255)),
                ('race_name', models.CharField(max_length=255)),
                ('Odds_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.odds')),
                ('RaceResult_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.raceresult')),
            ],
        ),
    ]
