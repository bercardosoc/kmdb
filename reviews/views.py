from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from reviews.serializers import ReviewSerializer
from rest_framework.authentication import TokenAuthentication
from project.pagination import CustomPageNumberPagination
from .permissions import ReviewPermissionsCustom
from .models import Review

def formatted_response(data):
    serializer_data = {
            **data,
            "user": {
                "id": data["user"]["id"],
                "first_name": data["user"]["first_name"],
                "last_name": data["user"]["last_name"]
            },
            "movie_id": data["movie"]["id"]
    }

    del serializer_data["movie"]

    return serializer_data

class ReviewView(APIView, CustomPageNumberPagination):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewPermissionsCustom]

    def get(self, request):
        reviews = Review.objects.all()

        result_page = self.paginate_queryset(reviews, request, view=self)

        serializer = ReviewSerializer(result_page, many=True)

        serializer_data = []

        for values in serializer.data:
            serializer_data.append(formatted_response(values))

        return self.get_paginated_response(serializer_data)

class ReviewViewDetail(APIView, CustomPageNumberPagination):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewPermissionsCustom]

    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie=movie_id)

        if not reviews:
            return Response({"message": "Movie review not found"}, status.HTTP_400_BAD_REQUEST)

        result_page = self.paginate_queryset(reviews, request, view=self)

        serializer = ReviewSerializer(result_page, many=True)

        serializer_data = []

        for values in serializer.data:
            serializer_data.append(formatted_response(values))

        return self.get_paginated_response(serializer_data)

    def post(self, request, movie_id):

        serializer = ReviewSerializer(data=request.data)    
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user.id, movie=movie_id)
        serializer_data = formatted_response(serializer.data)
        return Response(serializer_data, status.HTTP_201_CREATED)

    def delete(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)

        self.check_object_permissions(request, review)

        review.delete()

        return Response({}, status.HTTP_204_NO_CONTENT)