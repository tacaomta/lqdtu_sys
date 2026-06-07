from django.urls import path
from .views import (
    login_view, 
    logout_view, 
    register_view, 
    profile_view,
    change_password_view
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("register/",register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path("change-password/", change_password_view, name="change_password"),
    path("author-link/", author_link_view, name="author_link"),
    path(
        "api/authors/search/",
        author_search_api,
        name="author_search_api"
    ),
    path(
        "api/publications/search/",
        publication_search_api,
        name="publication_search_api"
    )
]