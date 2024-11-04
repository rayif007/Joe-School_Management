from django.urls import path
from . import views

# Namespace for the app (recommended for URL resolution)
app_name = 'school_app'

urlpatterns = [
    # Public Pages
    path('', views.home, name='home'),
    
    # Authentication URLs
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Student Management URLs
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:id>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:id>/delete/', views.delete_student, name='delete_student'),
    
    # Library Management URLs
    path('library/', views.library_list, name='library_list'),
    path('library/add/', views.add_library_record, name='add_library_record'),
    
    # Fees Management URLs
    path('fees/', views.fees_list, name='fees_list'),
    path('fees/add/', views.add_fees_record, name='add_fees_record'),
]




