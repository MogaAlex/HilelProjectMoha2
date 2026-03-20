from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.TextField()
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books',
                                 null=True, blank=True)
    def __str__(self):
        return f'{self.title} - {self.author}'

