# Generated by Django 4.1.7 on 2023-04-03 11:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальное количество ингредиента: 1 ед.'), django.core.validators.MaxValueValidator(3000, message='Максимальное количество ингредиента: 3000 ед.')], verbose_name='Количество ингредиента'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальное время приготовления в минутах: 1'), django.core.validators.MaxValueValidator(360, message='Максимальное время приготовления в минутах: 360')], verbose_name='Время в мин.'),
        ),
    ]
