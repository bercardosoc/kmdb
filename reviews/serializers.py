from django.shortcuts import get_object_or_404
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from movies.models import Movie
from reviews.models import Review
from users.models import User

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = "__all__"
        extra_kwargs = {'stars': {'validators':[MinValueValidator(1), MaxValueValidator(10)]}}
        depth = 1

    def create(self, validated_data):

        user = get_object_or_404(User, pk=validated_data["user"])
        movie = get_object_or_404(Movie, pk=validated_data["movie"])


        validated_data["user"] = user
        validated_data["movie"] = movie
        review = Review.objects.create(**validated_data)

        return review