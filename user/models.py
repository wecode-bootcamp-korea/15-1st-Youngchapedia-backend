from django.db              import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils           import timezone


class Language(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'languages'


class Country(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'countries'


class Disclosure(models.Model):
    name  = models.CharField(max_length=10)
    class Meta:
        db_table = 'dislosures'


class User(models.Model):
    email            = models.CharField(max_length=45)
    password         = models.CharField(max_length=250)
    profile_image    = models.CharField(max_length=1000, null=True)
    user_bio         = models.TextField(max_length=300, null=True)
    language         = models.ForeignKey(Language, on_delete=models.SET_DEFAULT, default=1)
    country          = models.ForeignKey(Country, on_delete=models.SET_DEFAULT, default=1)
    disclosure_scope = models.ForeignKey(Disclosure, on_delete=models.SET_DEFAULT, default=1)
    background_image = models.CharField(max_length=1000, null=True)
    username         = models.CharField(max_length=20)
    relations        = models.ManyToManyField('self', through='Relation', symmetrical=False)
    class Meta:
        db_table = 'users'


class RelationStatus(models.Model):
    status = models.CharField(max_length=20)
    class Meta:
        db_table = 'relation_status'


class Relation(models.Model):
    from_user       = models.ForeignKey(User, on_delete = models.CASCADE, related_name='relations_by_from_user')
    to_user         = models.ForeignKey(User, on_delete = models.CASCADE, related_name='relations_by_to_user')
    relation_status = models.ForeignKey(RelationStatus, on_delete = models.CASCADE)
    class Meta:
        db_table = 'relations'


class Partner(models.Model):
    request_user   = models.ForeignKey(User, on_delete = models.CASCADE, related_name='requested_user_id')
    requested_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='request_user_id')
    request_status = models.BooleanField()
    class Meta:
        db_table = 'partners'


class Category(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'categories'


class Content(models.Model):
    title_korean = models.CharField(max_length=100)
    main_photo   = models.CharField(max_length=1000)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    release_year = models.IntegerField(default=0000, null=True)
    class Meta:
        db_table = 'contents'


class Rating(models.Model):
    user        = models.ForeignKey(User, on_delete = models.CASCADE, related_name='rated_movie')
    content     = models.ForeignKey(Content, on_delete = models.CASCADE, related_name='rating_user')
    rating      = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])
    watch_date  = models.DateField(null=True) 
    create_time = models.DateTimeField(default = timezone.now)
    class Meta:
        db_table = 'ratings'


class ArchiveType(models.Model):
    name = models.CharField(max_length=10)
    class Meta:
        db_table = 'archivetypes'


class Archive(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archives')
    content      = models.ForeignKey(Content, on_delete=models.CASCADE)
    archive_type = models.ForeignKey(ArchiveType, on_delete=models.CASCADE)
    created_at   = models.DateTimeField(timezone.now)
    updated_at   = models.DateTimeField()
    class Meta:
        db_table = 'archives'


class MovieOverview(models.Model):
    title_original = models.CharField(max_length=100)
    runtime        = models.IntegerField(default=0, null=True)
    description    = models.TextField(max_length=200, null=True)
    content        = models.ForeignKey(Content, on_delete=models.CASCADE)
    class Meta:
        db_table = 'movie_overviews'


class TvProgramOverview(models.Model):
    title_original = models.CharField(max_length=100)
    broadcast      = models.CharField(max_length=45, null=True)
    description    = models.TextField(null=True)
    content        = models.ForeignKey(Content, on_delete=models.CASCADE)
    class Meta:
        db_table = 'tv_program_overviews'


class SubCategory(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        db_table = 'subcategories'


class BookOverview(models.Model):
    sub_title              = models.CharField(max_length=45)
    sub_category           = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    page                   = models.IntegerField(default=0, null=True)
    book_contents          = models.TextField(max_length=1000, null=True)
    publisher_introduction = models.TextField(max_length=1000, null=True)
    content                = models.ForeignKey(Content, on_delete=models.CASCADE)
    class Meta:
        db_table = 'book_overviews'


class ContentPhoto(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    photo   = models.CharField(max_length=1000)
    class Meta:
        db_table = 'content_photos'


class People(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(null=True)
    class Meta:
        db_table = 'people'


class Job(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'jobs'


class PeopleJob(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    job    = models.ForeignKey(Job, on_delete=models.CASCADE)
    class Meta:
        db_table = 'people_jobs'


class Staff(models.Model):
    name      = models.ForeignKey(People, on_delete=models.CASCADE)
    content   = models.ForeignKey(Content, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=50, null=True)
    class Meta:
        db_table = 'staffs'


class StaffJobs(models.Model):
    staff   = models.ForeignKey(Staff, on_delete=models.CASCADE)
    job     = models.ForeignKey(Job, on_delete=models.CASCADE)
    class Meta:
        db_table = 'staff_jobs'


class Genre(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'genres'


class ContentGenre(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    genre   = models.ForeignKey(Genre, on_delete=models.CASCADE)
    class Meta:
        db_table = 'content_genres'


class ContentCountry(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    class Meta:
        db_table = 'content_countries'


class ContentService(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        db_table = 'content_services'


class ContentAvailableService(models.Model):
    content         = models.ForeignKey(Content, on_delete=models.CASCADE)
    content_service = models.ForeignKey(ContentService, on_delete=models.CASCADE)
    price           = models.IntegerField(null=True)
    link            = models.URLField(max_length=1000)
    class Meta:
        db_table = 'contents_available_services'


class Tag(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        db_table = 'tags'


class ContentTag(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    tag     = models.ForeignKey(Tag, on_delete=models.CASCADE)
    class Meta:
        db_table = 'content_tags'


class Review(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    content     = models.ForeignKey(Content, on_delete=models.CASCADE)
    body        = models.TextField(max_length=1000)
    created_at  = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'reviews'


class ReviewLike(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    review     = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'review_likes'


class ReviewReport(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    review     = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'review_reports'


class ReviewComment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    review     = models.ForeignKey(Review, on_delete=models.CASCADE)
    body       = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'review_comments'


class ReviewCommentLike(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    comment    = models.ForeignKey(ReviewComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'review_comment_likes'


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
    created_at = models.TimeField(default=timezone.now)
    class Meta:
        db_table = 'collection_comment_likes'


