from django.db.models import Avg

from archive.models import Rating

def calculate_ratings(content_pk):
    return  Rating.objects.filter(content_id = content_pk).aggregate(Avg('rating'))
