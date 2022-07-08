from django.db import models

# Create your models here.

class ChoicesReview(models.TextChoices):

    MUST_WATCH = ("must watch",)
    SHOULD_WATCH = ("should watch",)
    AVOID_WATCH = ("avoid watch",)
    NO_OPINION = ("no opinion",)

class Review(models.Model):

    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField()
    recommendation = models.CharField(
        max_length=50,
        choices=ChoicesReview.choices,
        default=ChoicesReview.NO_OPINION,
    )

    user = models.ForeignKey(
        "users.User", related_name="user", on_delete=models.CASCADE
    )

    movie = models.ForeignKey(
        "movies.Movie", related_name="movie", on_delete=models.CASCADE
    )