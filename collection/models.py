from django.db    import models
from django.utils import timezone

from user.models    import User
from content.models import Content


class Collection(models.Model):
     user       = models.ForeignKey(User, on_delete=models.CASCADE)
     title      = models.CharField(max_length=40)
     created_at = models.DateTimeField(default=timezone.now)
     updated_at = models.DateTimeField()
     class Meta:
         db_table = 'collections'


class ContentCollection(models.Model):
    content    = models.ForeignKey(Content, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    class Meta:
        db_table = 'content_collections'


class CollectionLike(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'collection_likes'


class CollectionComment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    body       = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'collection_comments'


class CollectionCommentLike(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    comment    = models.ForeignKey(CollectionComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'collection_comment_likes'
