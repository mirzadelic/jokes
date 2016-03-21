from __future__ import unicode_literals
from django.db import models
from django.db.models import Avg
from django.template.defaultfilters import truncatewords
from managers import JokeManager
from decimal import Decimal

TWOPLACES = Decimal(10) ** -2
RATE_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = 'kategorija'
        verbose_name_plural = 'kategorije'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Joke(models.Model):
    text = models.TextField(max_length=1000, blank=False)
    category = models.ForeignKey(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    creator = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=150, blank=True, null=True)

    objects = models.Manager()
    active = JokeManager()

    def __str__(self):
        return truncatewords(self.text, 30)

    def __unicode__(self):
        return truncatewords(self.text, 30)

    def get_likes_count(self):
        return self.likes.count()
    get_likes_count.short_description = 'Broj lajkova'

    def get_ratings_count(self):
        return self.ratings.count()
    get_ratings_count.short_description = 'Broj glasova'

    def get_rating_score(self):
        score = self.ratings.aggregate(Avg('rate'))['rate__avg']
        if score is None:
            score = 0.0
        return Decimal(score).quantize(TWOPLACES)
    get_rating_score.short_description = 'Ocena glasanja'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'vic'
        verbose_name_plural = 'vicevi'


class Like(models.Model):
    joke = models.ForeignKey(Joke, related_name='likes')
    device_id = models.CharField(max_length=100)

    class Meta:
        unique_together = ('joke', 'device_id')
        verbose_name = 'lajk'
        verbose_name_plural = 'lajkovi'


class Rating(models.Model):
    joke = models.ForeignKey(Joke, related_name='ratings')
    rate = models.CharField(max_length=1, choices=RATE_CHOICES)
    device_id = models.CharField(max_length=100)

    class Meta:
        unique_together = ('joke', 'device_id')
        verbose_name = 'ocena'
        verbose_name_plural = 'ocene'
