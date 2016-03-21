from django.contrib import admin
from models import *
from forms import *


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0


class JokeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at', 'approved', 'get_likes_count', 'get_rating_score')
    list_editable = ('approved',)
    list_filter = ('approved',)
    form = JokeAdminForm

    inlines = [
        LikeInline,
        RatingInline,
    ]

admin.site.register(Joke, JokeAdmin)
admin.site.register(Category)
