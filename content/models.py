from django.db import models

from user.models import Country


class Category(models.Model):
     name = models.CharField(max_length=45)
     class Meta:
         db_table = 'categories'


class Content(models.Model):
    title_korean   = models.CharField(max_length=100)
    main_image_url = models.URLField("Content Main Image URL", null=True)
    category       = models.ForeignKey(Category, on_delete=models.CASCADE)
    release_year   = models.IntegerField(default=0000, null=True)
    class Meta:
        db_table = 'contents'


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


class BookCategory(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        db_table = 'book_categories'


class BookOverview(models.Model):
    sub_title              = models.CharField(max_length=45)
    book_category          = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    page                   = models.IntegerField(default=0, null=True)
    book_contents          = models.TextField(max_length=1000, null=True)
    publisher_introduction = models.TextField(max_length=1000, null=True)
    content                = models.ForeignKey(Content, on_delete=models.CASCADE)
    class Meta:
        db_table = 'book_overviews'


class ContentPhoto(models.Model):
    content   = models.ForeignKey(Content, on_delete=models.CASCADE)
    photo_url = models.URLField("Content Photo URL")
    class Meta:
        db_table = 'content_photos'


class People(models.Model):
    name              = models.CharField(max_length=100)
    profile_image_url = models.URLField(default='')
    description       = models.TextField(null=True)
    class Meta:
        db_table = 'people'


class Job(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'jobs'


class ContentPeople(models.Model):
    people    = models.ForeignKey(People, on_delete=models.CASCADE)
    content   = models.ForeignKey(Content, on_delete=models.CASCADE)
    job       = models.ForeignKey(Job, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=50, null=True)
    class Meta:
        db_table = 'content_people'


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

