from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from recipes.constants import MAX_VALUE, MIN_TIME, MIN_VALUE, LENGHT

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=128)
    measurement_unit = models.CharField('Единица измерения', max_length=64)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, ед. измерения - {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField('Название', max_length=32, unique=True)
    slug = models.SlugField('Слаг', max_length=32, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


def image_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.name, extension)
    return "rescipes/images/{}__{}".format(instance.author.username, filename)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField('Название', max_length=100)
    image = models.ImageField(
        'Изображение',
        upload_to=image_directory_path,
        blank=True,  # TODO: убрать
        null=True
    )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингридиенты',
        related_name='ingredients'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Тег')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(
                MIN_TIME,
                f'Время приготовления не должно быть меньше {MIN_TIME}'
            )
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = '-pub_date',

    def __str__(self):
        return f'{self.name}, автор - {self.author}'


class ShortLinkConverter(models.Model):
    recipe = models.OneToOneField(
        Recipe,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Рецепт')
    short_link = models.CharField(
        'Короткая ссылка',
        max_length=LENGHT,
        db_index=True,
        unique=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Конвентатор коротких ссылок'
        verbose_name_plural = 'Конвентаторы коротких ссылок'

    def __str__(self):
        return f'{self.recipe.name} -> {self.short_link}'


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe',
        verbose_name='Ингридиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                MIN_VALUE, f'Количество не может быть меньше {MIN_VALUE}'),
            MaxValueValidator(
                MAX_VALUE, f'Количество не может быть больше {MAX_VALUE}')
        ]
    )

    class Meta:
        verbose_name = 'Ингридиенты рецепта'
        verbose_name_plural = 'Ингридиенты рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredients'),
                name='unique_recipe_ingredients'
            )
        ]

    def __str__(self):
        return (
            f'{self.recipe.name}, ингридиент: {self.ingredients.name} '
            f'{self.amount} {self.ingredients.measurement_unit}'
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            )
        ]

    def __str__(self):
        return f'"{self.recipe}" в Избранном у {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_list'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в списке покупок пользователя {self.user}'
