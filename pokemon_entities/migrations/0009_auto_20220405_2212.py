# Generated by Django 3.1.14 on 2022-04-05 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0008_auto_20220405_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_entity', to='pokemon_entities.pokemon', verbose_name='Покемон'),
        ),
    ]
