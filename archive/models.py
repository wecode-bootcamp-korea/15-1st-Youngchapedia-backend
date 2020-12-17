from django.db              import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils           import timezone

from user.models    import User
from content.models import Content


class Rating(models.Model):
     user        = models.ForeignKey(User, on_delete = models.CASCADE, related_name='rated_movie')
     content     = models.ForeignKey(Content, on_delete = models.CASCADE, related_name='rating_user')
     rating      = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])
     watch_date  = models.DateField(null=True)
     created_at  = models.DateTimeField(default = timezone.now)
     updated_at  = models.DateTimeField(default = timezone.now)
     class Meta:
         db_table = 'ratings'


class ArchiveType(models.Model):
    name = models.CharField(max_length=10)
    class Meta:
        db_table = 'archive_types'


class Archive(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archives')
    content      = models.ForeignKey(Content, on_delete=models.CASCADE)
    archive_type = models.ForeignKey(ArchiveType, on_delete=models.CASCADE)
    created_at   = models.DateTimeField(timezone.now)
    updated_at   = models.DateTimeField()
    class Meta:
        db_table = 'archives'

