from django.db import models
from django.contrib.auth.models import User
from .validators import real_age
from django.urls import reverse


class Tag(models.Model):
    tag = models.CharField('Тег', max_length=20)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    birthday = models.DateField('Дата рождения', validators=[real_age])
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
        help_text='Удерживайте Ctrl для выбора нескольких вариантов'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор записи',
        null=True,
        blank=False,
        related_name='birthdays'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )

        verbose_name = 'день рождения'
        verbose_name_plural = 'Дни рождения'

    def __str__(self):
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.first_name

    def get_absolute_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.pk})


class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    birthday = models.ForeignKey(
        Birthday,
        on_delete=models.CASCADE,
        related_name='congratulations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
