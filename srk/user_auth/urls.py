from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='user_auth'),
    path("home",views.home,name='home'),
    path("register",views.register,name='register'),
    path("diversity",views.diversity,name='diversity'),
    path("ad_info",views.ad_info,name='ad_info'),
    path("report",views.report,name='report'),
    path("fields",views.fields,name='fields'),
    path("admin_register",views.admin_register,name='admin_register'),
    path("admin_login",views.admin_login_view,name='admin_login'),
    path("admin_dashboard",views.admin_dashboard,name='admin_dashboard'),
    path("admin_logout",views.admin_logout,name='admin_logout'),
    path('project_detail/', views.project_detail, name='project_detail'),
    path("edit_project/<int:project_id>/", views.edit_project, name="edit_project"),
    path("delete_project/<int:project_id>/", views.delete_project, name="delete_project"),
]