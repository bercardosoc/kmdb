from rest_framework import serializers
from genres.models import Genre
from movies.models import Movie
from genres.serializers import GenreSerializer
class MovieSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    duration = serializers.CharField()
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data):

        genres = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)

        for genre in genres:

            genre, _ = Genre.objects.get_or_create(**genre)
            movie.genres.add(genre)

        return movie 

    def update(self, instance, validated_data):

        for key, value in validated_data.items():

            if key == "genres":
                raise KeyError(key)

            else:
                setattr(instance, key, value)

        instance.save()
        return instance 