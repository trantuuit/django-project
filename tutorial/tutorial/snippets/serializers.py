from snippets.models import (
    UserModel, MovieModel, CFModel, SModel, UPModel, LAModel, WIPModel
)
from rest_framework import serializers

from django_cassandra_engine.rest.serializers import DjangoCassandraModelSerializer


class UserModelSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = UserModel
        fields = '__all__'

class MovieModelSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = MovieModel
        fields = '__all__'

class CFModelSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = CFModel
        fields = '__all__'

class SModelSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = SModel
        fields = '__all__'


class UPModelSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = UPModel
        fields = '__all__'


class LAModelSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = LAModel
        fields = '__all__'


class WIPModelSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = WIPModel
        fields = '__all__'

