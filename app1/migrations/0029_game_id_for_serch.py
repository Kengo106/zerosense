# Generated by Django 4.2.1 on 2023-09-20 16:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0028_rename_gamerule_game_game_rule_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='id_for_serch',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]