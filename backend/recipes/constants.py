from string import ascii_letters, digits

# Максимумы для названия и единицы измерения ингредиента
NAME_INGREDIENT = 128
MEASURE_MAX = 64

# Максимумы для названия и слага тега
NAME_TAG = 32
SLUG_TAG = 32

# Максимум для длины названия рецепта
NAME_RECIPE = 100

# Значения для количества ингредиентов
MAX_AMOUNT = 32_000
MIN_AMOUNT = 1

# Значения для времени приготовления
MAX_TIME = 32_000
MIN_TIME = 1

# Длина укороченной ссылки
LENGTH = 3

# Символы, из которых состоит короткая ссылка
CHARACTERS = ascii_letters + digits


# Максимумы для имени и фамилии пользователя
FIRST_NAME = 150
LAST_NAME = 150
