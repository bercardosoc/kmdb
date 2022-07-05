from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status

from movies.models import Movie
from movies.serializers import MovieSerializer

class MovieView(APIView):

    def get(self, _: Request):

        movies = Movie.objects.all()
        serialized = MovieSerializer(instance=movies, many=True)

        return Response({
            "movies": serialized.data
        }, status.HTTP_200_OK)

    def post(self, request: Request):

        serialized = MovieSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status.HTTP_201_CREATED)