from django.conf import settings
from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=settings.DEFAULT_FIELD_LENGTH)
    color = models.CharField(
        'Цвет в формате HEX',
        max_length=settings.HEX_LENGTH,
        null=True,
        validators=[
            RegexValidator(
                regex="^#([A-Fa-f0-9]{6})$",
                message='Формат HEX: #______',
            )
        ],
    )
    slug = models.SlugField(
        max_length=settings.DEFAULT_FIELD_LENGTH,
        null=True,
        unique=True
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=settings.DEFAULT_FIELD_LENGTH,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=settings.DEFAULT_FIELD_LENGTH,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient_unit'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(
        'Название',
        max_length=settings.DEFAULT_FIELD_LENGTH
    )
    text = models.TextField(
        'Описание'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    image = models.ImageField(
        'Изображение',
        upload_to='images/',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты',
    )
    cooking_time = models.IntegerField(
        'Время в мин.',
        validators=[
            MinValueValidator(
                settings.MIN_VALUE,
                message=(
                    f'Минимальное время приготовления в минутах: '
                    f'{settings.MIN_VALUE}'
                )
            ),
            MaxValueValidator(
                settings.MAX_COOKING_TIME,
                message=(
                    f'Максимальное время приготовления в минутах: '
                    f'{settings.MAX_COOKING_TIME}'
                )
            )
        ]
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_recipe'
            )
        ]

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientinrecipe',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        'Количество ингредиента',
        validators=[
            MinValueValidator(
                settings.MIN_VALUE,
                message=(
                    f'Минимальное количество ингредиента: '
                    f'{settings.MIN_VALUE} ед.'
                )
            ),
            MaxValueValidator(
                settings.MAX_AMOUNT,
                message=(
                    f'Максимальное количество ингредиента: '
                    f'{settings.MAX_AMOUNT} ед.'
                )
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_recipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient}-{self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favouring',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user}-{self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            )
        ]
