from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True)

    def __str__(self):
        return f'{self.category}'

    def get_absolute_url(self):
        return reverse('secondboard:board_category', args=[self.slug])


class Board(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    authors = models.ForeignKey(
        User, related_name='second', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='buyphotos', blank=True)
    text = models.TextField()
    date = models.DateField()
    slug = models.SlugField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return f'{self.authors.username}'

    def get_absolute_url(self):
        return reverse('secondboard:board_detail', args=[str(self.id)])
