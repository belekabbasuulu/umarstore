from django.db import models
from django.urls import reverse
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse('listings:product_list_by_category', args=[self.slug])

    class Meta:
        ordering = ('-name',)
        verbose_name_plural = 'categoriess'

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('-name',)
        verbose_name_plural = 'seasons'

    def __str__(self):
        return self.name


GENDER = [
    ('Женская', 'Female'),
    ('Мужская', 'Male')
]


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    seasons = models.ForeignKey(
        Season, related_name='products', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    color = models.ManyToManyField('Color', verbose_name="Цвет")
    size = models.ManyToManyField('Size', verbose_name="Размер")
    image = models.ImageField(upload_to='products')
    gender = models.CharField(max_length=50, choices=GENDER, default='Женская')
    articul = models.CharField(max_length=100, unique=True, null=True)
    description = models.TextField()
    brand = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=150, null=True)
    material_podoshvy = models.CharField(max_length=100, null=True)
    material_stelki = models.CharField(max_length=100, null=True)
    top_height = models.IntegerField(blank=True, null=True)
    kabluk_height = models.IntegerField(blank=True, null=True)
    material_top = models.CharField(max_length=100, null=True)
    material_podkladki = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('listings:product_detail', args=[self.category.slug, self.slug])

    def get_average_review_score(self):
        average_score = 0.0
        if self.reviews.count() > 0:
            total_score = sum([review.rating for review in self.reviews.all()])
            average_score = total_score / self.reviews.count()
        return round(average_score, 1)

    class Meta:
        ordering = ('updated',)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name='reviews', on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.pk)


class Color(models.Model):
    name = models.CharField("Название", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class Size(models.Model):
    size = models.CharField("Название", max_length=20, unique=True)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"
