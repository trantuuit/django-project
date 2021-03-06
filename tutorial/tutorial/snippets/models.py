from __future__ import unicode_literals
# from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

#User model
class UserModel(DjangoCassandraModel):
    idx = columns.Integer(index=True)
    user_id = columns.Text(primary_key=True)
    email = columns.Text(required=False)
    password = columns.Text(required=True)
    first_name = columns.Text(required=False)
    last_name = columns.Text(required=False)
    url = columns.Text(required=False)
    isnew = columns.Integer(required=True)
    survey = columns.List( columns.Text, required=False )
    class Meta:
        get_pk_field = 'user_id'

#Movie model
#idx,
# movieId,
# title,
# genres,
# directors,
# writers,
# actors,
# description,
# year,
# countries,
# release,
# runtime,
# rating,
# keywords,
# poster,
# slate
class MovieModel(DjangoCassandraModel):
    idx = columns.Integer( index=True )
    movie_id = columns.Text( primary_key=True )
    title = columns.Text( required=False )
    genres = columns.List( columns.Text, required=False )
    directors = columns.List( columns.Text, required=False )
    writers = columns.List( columns.Text, required=False )
    actors = columns.List( columns.Text, required=False ) 
    description = columns.Text( required=False )
    year = columns.Text(required=False)
    countries = columns.List( columns.Text, required=False ) 
    release = columns.Text(required=False)
    runtime = columns.Text(required=False)
    rating = columns.Text(required=False)
    keywords = columns.List( columns.Text, required=False ) 
    poster = columns.Text( required=False )
    slate = columns.Text( required=False )
    class Meta:
        get_pk_field = 'movie_id'

#Collaborative filtering model

class CFModel(DjangoCassandraModel):
    idx_user = columns.Integer( primary_key=True )
    recommendations = columns.List( columns.Text, required=False )
    class Meta:
        get_pk_field = 'idx_user'
    

#Similarity model
class SModel(DjangoCassandraModel):
    movie_id = columns.Text( primary_key=True )
    recommendations = columns.List( columns.Text, required=False )
    class Meta:
        get_pk_field = 'movie_id'

#User profile model
class UPModel(DjangoCassandraModel):
    idx_user = columns.Integer( primary_key=True )
    recommendations = columns.List( columns.Text, required=False )

#Last action model
class LAModel(DjangoCassandraModel):
    idx_user = columns.Integer( primary_key=True )
    recommendations = columns.List( columns.Text, required=False )
    class Meta:
        get_pk_field = 'idx_user'

#What is popular model
class WIPModel(DjangoCassandraModel):
    bucket= columns.Integer( primary_key=True)
    views = columns.Integer( primary_key=True, clustering_order='DESC')
    movie_id = columns.Text( primary_key=True )
    class Meta:
        get_pk_field = 'movie_id'

#What is popular model
class TrendModel(DjangoCassandraModel):
    bucket = columns.Integer( primary_key=True)
    rank = columns.Integer( primary_key=True, clustering_order='ASC')
    movie_id = columns.Text( primary_key=True )
    class Meta:
        get_pk_field = 'movie_id'

class SpecificProfileModel(DjangoCassandraModel):
    identifier = columns.Text( primary_key=True )
    recommendations = columns.List( columns.Text, required=False )
    class Meta:
        get_pk_field = 'identifier'

class GenresProfileModel(DjangoCassandraModel):
    idx_user = columns.Integer( primary_key=True )
    recommendations = columns.List( columns.Text, required=False )
    class Meta:
        get_pk_field = 'idx_user'

class ActorsProfileModel(DjangoCassandraModel):
    idx_user = columns.Integer( primary_key=True )
    recommendations = columns.List( columns.Text, required=False )
    class Meta:
        get_pk_field = 'idx_user'

class WritersProfileModel(DjangoCassandraModel):
    idx_user = columns.Integer( primary_key=True )
    recommendations = columns.List( columns.Text, required=False )
    class Meta:
        get_pk_field = 'idx_user'

class DirectorsProfileModel(DjangoCassandraModel):
    idx_user = columns.Integer( primary_key=True )
    recommendations = columns.List( columns.Text, required=False )
    class Meta:
        get_pk_field = 'idx_user'

class UserEventModel(DjangoCassandraModel):
    idx_user = columns.Integer( primary_key=True )
    time = columns.BigInt( primary_key=True, clustering_order='DESC' )
    idx_movie = columns.Integer( primary_key =True )
    movie_id = columns.Text( required=False )
    type_event = columns.Text( required=False )
    value = columns.Float( required=False)
    class Meta:
        get_pk_field = 'idx_user'


class LastLikeModel(DjangoCassandraModel):
    idx_user = columns.Integer( primary_key=True )
    time = columns.Integer( required=True)
    idx_movie = columns.Integer( required=True )
    class Meta:
        get_pk_field = 'idx_user'

class LastWatchModel(DjangoCassandraModel):
    idx_user = columns.Integer( primary_key=True )
    recommendations = columns.List(columns.Text, required=True)
    class Meta:
        get_pk_field = 'idx_user'





