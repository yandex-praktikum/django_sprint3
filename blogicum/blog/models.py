from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class AbstractBlogModel(models.Model):
    """Абстрактная модель с флагом "Опубликовано" и датой создания поста"""

    is_published = models.BooleanField(
        default=True, verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
        ordering = ('created_at', )


class Category(AbstractBlogModel):
    """Модель, определяющая категории постов"""

    title = models.CharField(
        max_length=settings.MAX_POST_LENGTH, verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(AbstractBlogModel):
    """Модель, определяющая местоположение создания постов"""

    name = models.CharField(
        max_length=settings.MAX_POST_LENGTH, verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(AbstractBlogModel):
    """Ссылающаяся модель, определяющая публикации и связанные модели"""

    title = models.CharField(
        max_length=settings.MAX_POST_LENGTH, verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='post'
    )

    class Meta:
        default_related_name = 'posts'
        ordering = ('-pub_date', )
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:25]
