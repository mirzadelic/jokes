from django.db import models


# manager for selecting only active jokes
class JokeManager(models.Manager):

    def get_queryset(self):
        qs = super(JokeManager, self).get_queryset()
        return qs.filter(approved=True)
