from django.db import models


# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    deleted = models.BooleanField(default=False, verbose_name="Удален")

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class NewsManager(models.Manager):

    def delete(self):
        pass

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

class News(BaseModel):
    objects = NewsManager()

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    preamble = models.CharField(max_length=1000, verbose_name='Вступление')
    body = models.TextField(verbose_name="Содержимое")
    body_as_markdown = models.BooleanField(default=False, verbose_name="Способ разметки")

    def __str__(self):
        return f'#{self.pk} {self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Course(BaseModel):
    name = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Description", **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="cost", default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name="cover")

    def __str__(self):
        return f"{self.pk} {self.name}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="Lesson number")
    title = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Description", **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)

    def __str__(self):
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('course', 'num')


class CoursesTeacher(BaseModel):
    courses = models.ManyToManyField(Course)
    name_first = models.CharField(max_length=128, verbose_name="Name")
    name_second = models.CharField(max_length=128, verbose_name="Surname")
    day_birth = models.DateField(verbose_name="Birth date")

    def __str__(self):
        return "{0:0>3} {1} {2}".format(self.pk, self.name_second, self.name_first)
