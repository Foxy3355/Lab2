from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import forms


class Author(models.Model):
    objects = None
    name = models.CharField(max_length=100, verbose_name='Имя', blank=False)
    lastName = models.CharField(max_length=100, verbose_name='Отчество', blank=True)
    middle_name = models.CharField(max_length=100, verbose_name='Фамилия', blank=False)
    dateOfBirth = models.DateField(max_length=100, verbose_name='Дата рождения', blank=False, null=False)

    def __str__(self):
        return '{} {} {}'.format(self.name, self.lastName, self.middle_name, )

    class Meta:
        unique_together = ('name', 'lastName', 'middle_name', 'dateOfBirth')
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Cover(models.Model):
    def validate_image(value):
        size_limit = 2 * 1024 * 1024
        if value.size > size_limit:
            raise forms.ValidationError('Файл слишком большой. Размер файла не должен превышать 2MB')

    cover = models.ImageField(validators=[validate_image], upload_to='cover/books/title', verbose_name='Изображения',
                              blank=True, null=False)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Book(models.Model):
    objects = None
    title = models.CharField(max_length=100, verbose_name='Название книги', blank=False, unique=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, max_length=100, verbose_name='Автор', blank=False)
    yearOfRel = models.IntegerField(verbose_name='Год выпуска', blank=False,
                                    validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    genre = models.CharField(max_length=100, verbose_name='Жанр', blank=True)
    category = models.CharField(max_length=100, blank=False, choices=[
        ('hud', 'Художественная литература'),
        ('uch', 'Учебник')
    ], default='hud')
    publisher = models.CharField(max_length=100, verbose_name='Издательство', blank=True)

    def validate_image(value):
        size_limit = 2 * 1024 * 1024
        if value.size > size_limit:
            raise forms.ValidationError('Файл слишком большой. Размер файла не должен превышать 2MB')

    photoPreview = models.ImageField(validators=[validate_image], upload_to='cover', verbose_name='Изображения',
                                     blank=True, null=True)
    bookFile = models.FileField(upload_to='books', verbose_name='Файл с книгой', blank=True, null=True)

    class Meta:
        unique_together = ('title', 'author', 'yearOfRel', 'publisher')
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
