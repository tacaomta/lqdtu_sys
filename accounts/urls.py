from django.urls import path
from .views import (
    login_view, 
    logout_view, 
    register_view, 
    profile_view,
    change_password_view,
    author_link_view,
    author_search_api,
    publication_search_api,
    create_author_link_request,
    author_link_request_list_view,
    approve_author_link_request,
    reject_author_link_request,
    approve_selected_author_link_requests,
    author_link_evidence_api,
    cancel_author_link_request,
    my_publications,
    user_list,
    toggle_user_status,
    create_user
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("register/",register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path("change-password/", change_password_view, name="change_password"),
    path("author-link/", author_link_view, name="author_link"),
    path("api/authors/search/", author_search_api, name="author_search_api"),
    path("api/publications/search/", publication_search_api, name="publication_search_api"),
    path("api/author-link/create/", create_author_link_request, name="create_author_link_request"),
    path("admin/author-link-requests/", author_link_request_list_view, name="author_link_request_list"),
    path("admin/author-link-request/<int:request_id>/approve/", approve_author_link_request, name="approve_author_link_request"),
    path("admin/author-link-request/<int:request_id>/reject/", reject_author_link_request, name="reject_author_link_request"),
    path("admin/author-link-request/approve-selected/", approve_selected_author_link_requests, name="approve_selected_author_link_requests"),
    path("admin/author-link-request/<int:request_id>/evidence/", author_link_evidence_api, name="author_link_evidence_api"),
    path("author-link-request/<int:request_id>/cancel/", cancel_author_link_request, name="cancel_author_link_request"),
    path("my-publications/", my_publications, name="my_publications"),
    path("admin/users/", user_list, name="user_list"),
    path("admin/users/<int:user_id>/toggle-status/", toggle_user_status, name="toggle_user_status"),
    path("admin/users/create/",create_user, name="create_user")
]