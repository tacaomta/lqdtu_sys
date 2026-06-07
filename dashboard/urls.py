from django.urls import path
from .views import (
    overview_view, 
    fields_view, 
    roles_view, 
    citations_view, 
    performance_view, 
    collaboration_view, 
    upload_csv, 
    transform_data, 
    transform_dashboard, 
    import_progress,
    settings_view,
    field_group_detail,
    save_field_group,
    apply_config,
    save_citation_groups
)

urlpatterns = [
    path('', overview_view, name='overview'),
    path('fields/', fields_view, name='fields'),
    path('citations/', citations_view, name='citations'),
    path('roles/', roles_view, name='roles'),
    path('performance/', performance_view, name='performance'),
    path('collaboration/', collaboration_view, name='collaboration'),
    path('upload/', upload_csv, name='upload_csv'),
    path("api/transform/", transform_data, name="transform_data"),
    path("transform/", transform_dashboard, name="transform_dashboard"),
    path("api/import-progress/<int:batch_id>/", import_progress, name="import_progress"),
    path("api/import-progress/<int:batch_id>/", import_progress, name="import_progress"),
    path('settings/', settings_view, name='settings_view'),
    path("settings/field-group/detail/<str:group_name>/", field_group_detail,name="field_group_detail"),
    path("settings/field-group/save/", save_field_group, name="save_field_group"),
    path("settings/apply-config/", apply_config, name="apply_config"),
    path("settings/citation-group/save/", save_citation_groups, name="save_citation_groups")
]