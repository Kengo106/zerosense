# Generated by Django 4.2.1 on 2023-07-29 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_game_gamerule_vote_gameresult_gamehorse_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameresult',
            name='race_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gameresult',
            name='JoinResultOdds',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.joinresultodds'),
        ),
    ]
