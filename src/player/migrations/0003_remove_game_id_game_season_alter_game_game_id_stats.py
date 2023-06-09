# Generated by Django 4.1.4 on 2023-01-26 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_game_home_point_game_visitors_point'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='id',
        ),
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='game_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField()),
                ('team_id', models.IntegerField()),
                ('points', models.IntegerField()),
                ('pos', models.CharField(max_length=10)),
                ('min', models.IntegerField()),
                ('fgm', models.IntegerField()),
                ('fga', models.IntegerField()),
                ('fgp', models.FloatField()),
                ('ftm', models.IntegerField()),
                ('fta', models.IntegerField()),
                ('ftp', models.IntegerField()),
                ('tpm', models.IntegerField()),
                ('tpa', models.IntegerField()),
                ('tpp', models.FloatField()),
                ('reb', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('pFouls', models.IntegerField()),
                ('steals', models.IntegerField()),
                ('turnovers', models.IntegerField()),
                ('blocks', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.game')),
            ],
        ),
    ]
