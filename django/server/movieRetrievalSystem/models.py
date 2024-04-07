# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actors(models.Model):
    actorid = models.CharField(db_column='ActorID', primary_key=True, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Actors'


class Directors(models.Model):
    directorid = models.CharField(db_column='DirectorID', primary_key=True, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Directors'


class Movie(models.Model):
    movieid = models.CharField(db_column='MovieID', primary_key=True)  # Field name made lowercase.
    primarytitle = models.CharField(db_column='primaryTitle', blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    originaltitle = models.CharField(db_column='originalTitle', blank=True, null=True)  # Field name made lowercase.
    runtimeminutes = models.IntegerField(db_column='runtimeMinutes', blank=True, null=True)  # Field name made lowercase.
    avgrating = models.IntegerField(db_column='avgRating', blank=True, null=True)  # Field name made lowercase.
    numvotes = models.IntegerField(db_column='numVotes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Movie'


class Movieactors(models.Model):
    movieid = models.OneToOneField(Movie, models.DO_NOTHING, db_column='MovieID', primary_key=True)  # Field name made lowercase.
    actorid = models.ForeignKey(Actors, models.DO_NOTHING, db_column='ActorID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MovieActors'


class Moviedirectors(models.Model):
    movieid = models.TextField(db_column='MovieID', blank=True, null=True)  # Field name made lowercase.
    directorid = models.TextField(db_column='DirectorID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MovieDirectors'


class Moviegenres(models.Model):
    movieid = models.OneToOneField(Movie, models.DO_NOTHING, db_column='MovieID', primary_key=True)  # Field name made lowercase.
    genrename = models.ForeignKey('Genres', models.DO_NOTHING, db_column='genreName', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MovieGenres'


class Genres(models.Model):
    genrename = models.TextField(db_column='genreName', primary_key=True, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'genres'
