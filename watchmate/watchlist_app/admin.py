from django.contrib import admin
from .models import StreamPlatform, WatchList, Review


@admin.register(StreamPlatform)
class StreamPlatformAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "about")


@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):

    list_display = ("id", "title", "story_line")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ("id", "rating", "watchlist")
