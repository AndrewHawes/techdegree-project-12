from django.urls import path

from projects import ajax, views

urlpatterns = [
    path('project/<int:pk>/', views.project_detail, name='project'),
    path('project_new/', views.CreateProjectView.as_view(), name='project_new'),
    path('project_edit/<int:pk>/', views.UpdateProjectView.as_view(), name='project_edit'),
    path('project_delete/<int:pk>/', views.DeleteProjectView.as_view(), name='project_delete'),
    path('applications/', views.applications, name='applications'),
]

ajax_urlpatterns = [
    path('applications/<str:status>/<int:pk>/', ajax.application_status,
         name='application_status'),
    path('positions/apply/<int:pk>/', ajax.apply_for_position, name='apply_for_position'),
]

urlpatterns += ajax_urlpatterns
