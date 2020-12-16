from django.db    import models
from django.utils import timezone


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
        db_table = 'disclosure'


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
    created_at       = models.DateTimeField(default = timezone.now)
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

