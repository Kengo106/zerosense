# Generated by Django 4.2.1 on 2023-07-26 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_rename_odds_id_joinresultodds_odds_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinresultodds',
            name='Odds',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app1.odds'),
        ),
        migrations.AlterField(
            model_name='joinresultodds',
            name='RaceResult',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app1.raceresult'),
        ),
    ]