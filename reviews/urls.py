from django.urls import path
from reviews.views import ReviewViewDetail, ReviewView

urlpatterns = [
    path("movies/<int:movie_id>/reviews/", ReviewViewDetail.as_view()),
    path("reviews/", ReviewView.as_view()),
    path("reviews/<int:review_id>", ReviewViewDetail.as_view())
]