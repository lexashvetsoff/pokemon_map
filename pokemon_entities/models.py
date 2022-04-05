from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя на русском')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Имя на английском')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Имя на японском')
    image = models.ImageField(blank=True, verbose_name='Картинка')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'Pokemon',
        verbose_name='Из кого эволюционирует',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='next_evolutions'
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    appeared_at = models.DateTimeField(verbose_name='Появится', blank=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет', blank=True)

    level = models.IntegerField(verbose_name='Уровень', blank=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True)
    strength = models.IntegerField(verbose_name='Прочность', blank=True)
    defence = models.IntegerField(verbose_name='Защита', blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', blank=True)
