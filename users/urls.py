from django.urls import path
from users.views import LoginView, UserView, UserViewDetail, UsersView

urlpatterns = [
    path("users/register/", UserView.as_view()),
    path("users/login/", LoginView.as_view()),
    path("users/", UsersView.as_view()),
    path("users/<int:user_id>", UserViewDetail.as_view())
]