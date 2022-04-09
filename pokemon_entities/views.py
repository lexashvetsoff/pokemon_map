import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        serialized_pokemon = {
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title,
        }
        if pokemon.image:
            serialized_pokemon['img_url'] = request.build_absolute_uri(pokemon.image.url)
        pokemons_on_page.append(serialized_pokemon)

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    serialized_pokemon = Pokemon.objects.get(id=pokemon_id)
    serialized_pokemon_entities = Pokemon.objects.get(id=pokemon_id).pokemon_entities.all()

    entities = []
    for pokemon_entity in serialized_pokemon_entities:
        entity = {
            "level": pokemon_entity.level,
            "lat": pokemon_entity.lat,
            "lon": pokemon_entity.lon,
        }
        entities.append(entity)
    
    if serialized_pokemon.previous_evolution:
        previous_evolution = {
            'title_ru': serialized_pokemon.previous_evolution.title,
            'pokemon_id': serialized_pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(serialized_pokemon.previous_evolution.image.url)
        }
    else:
        previous_evolution = ''

    next_pokemon = Pokemon.objects.get(id=pokemon_id).next_evolutions.first()
    if next_pokemon:
        next_evolution = {
            'title_ru': next_pokemon.title,
            'pokemon_id': next_pokemon.id,
            'img_url': request.build_absolute_uri(next_pokemon.image.url)
        }
    else:
        next_evolution = ''
    
    pokemon = {
        "pokemon_id": serialized_pokemon.id,
        "title_ru": serialized_pokemon.title,
        "title_en": serialized_pokemon.title_en,
        "title_jp": serialized_pokemon.title_jp,
        "description": serialized_pokemon.description,
        "img_url": request.build_absolute_uri(serialized_pokemon.image.url),
        "entities": entities,
        "previous_evolution": previous_evolution,
        "next_evolution": next_evolution
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon['entities']:
        add_pokemon(
            folium_map, pokemon_entity['lat'],
            pokemon_entity['lon'],
            pokemon['img_url']
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
