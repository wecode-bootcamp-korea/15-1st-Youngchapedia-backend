from django.db    import models
from django.utils import timezone

from user.models    import User
from content.models import Content


class Review(models.Model):
     user        = models.ForeignKey(User, on_delete=models.CASCADE)
     content     = models.ForeignKey(Content, on_delete=models.CASCADE)
     body        = models.TextField(max_length=1000)
     created_at  = models.DateTimeField(auto_now_add=True)
     updated_at  = models.DateTimeField(auto_now=True)
     class Meta:
         db_table = 'reviews'


class ReviewLike(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    review     = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='liked_users')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'review_likes'


class ReviewReport(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    review     = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'review_reports'


class ReviewComment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    review     = models.ForeignKey(Review, on_delete=models.CASCADE)
    body       = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'review_comments'


class ReviewCommentLike(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    comment    = models.ForeignKey(ReviewComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'review_comment_likes'

