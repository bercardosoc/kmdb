from multiprocessing.sharedctypes import Value
from rest_framework import serializers, status 
from genres.models import Genre

class GenreSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):

        genre, created = Genre.objects.get_or_create(**validated_data)

        if not created:

            raise ValueError(
                {"message": f"`{validated_data['name']}` already exists."}, status.HTTP_409_CONFLICT
            )

        return genre 