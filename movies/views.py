from django.http import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Request, Response, status
from yaml import serialize

from movies.models import Movie
from movies.permissions import MyCustomPermission
from movies.serializers import MovieSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

class MovieView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [MyCustomPermission]

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

class MovieViewDetail(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [MyCustomPermission]

    def get(self, request, movie_id):

        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, movie_id):

        try: 
            movie = get_object_or_404(Movie, pk=movie_id)

            serialized = MovieSerializer(instance=movie, data=request.data, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()

            return Response(serialized.data, status.HTTP_200_OK)

        except KeyError as key:

            return Response(
                {"message": f"You can not update {key} property"},
                status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        except Http404:
            return Response({"error": "Movie not found"})

    def delete(self, request, movie_id):

        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()

        return Response(status.HTTP_204_NO_CONTENT)