from django.db.models import Avg

from archive.models import Rating

def ratings_calc(content_pk):
    ratings = Rating.objects.filter(content_id = content_pk)
    average_rating = ratings.aggregate(Avg('rating'))
    return average_rating
