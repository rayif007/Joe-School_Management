from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Student, LibraryHistory, FeesHistory
from .forms import CustomUserCreationForm, LoginForm, StudentForm, LibraryRecordForm, FeesHistoryForm

# Home view
def home(request):
    return render(request, 'school_app/home.html')

# Login view
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('school_app:dashboard')  # Include namespace here
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'school_app/login.html', {'form': form})

# Register view
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('school_app:dashboard')  # Redirect to the dashboard
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'school_app/register.html', {'form': form})

# Logout view
@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('school_app:login_user')  # Redirect to the login page

# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'school_app/dashboard.html')

# Student list view
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'school_app/student_list.html', {'students': students})

# Add student view (admin and staff only)
@login_required
def add_student(request):
    if request.user.role not in ['admin', 'staff']:
        messages.warning(request, "You do not have permission to add students.")
        return redirect('school_app:dashboard')  # Include namespace here

    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Student added successfully.")
        return redirect('school_app:student_list')  # Include namespace here
    
    return render(request, 'school_app/add_student.html', {'form': form})

# Edit student view (admin and staff only)
@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    
    if request.user.role not in ['admin', 'staff']:
        messages.warning(request, "You do not have permission to edit students.")
        return redirect('school_app:dashboard')  # Include namespace here

    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, "Student details updated successfully.")
        return redirect('school_app:student_list')  # Include namespace here
    
    return render(request, 'school_app/edit_student.html', {'form': form})

# Delete student view (admin only)
@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    
    if request.user.role != 'admin':
        messages.warning(request, "You do not have permission to delete students.")
        return redirect('school_app:dashboard')  # Include namespace here

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect('school_app:student_list')  # Include namespace here
    
    return render(request, 'school_app/delete_student.html', {'student': student})

# Library list view
@login_required
def library_list(request):
    library_records = LibraryHistory.objects.select_related('student', 'book').all()
    return render(request, 'school_app/library_list.html', {'library_records': library_records})

# Add library record view (librarian only)
@login_required
def add_library_record(request):
    if request.user.role != 'librarian':
        messages.warning(request, "You do not have permission to add library records.")
        return redirect('school_app:dashboard')  # Include namespace here

    form = LibraryRecordForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Library record added successfully.")
        return redirect('school_app:library_list')  # Redirect to the library list view
    
    return render(request, 'school_app/add_library_record.html', {'form': form})

# Fees list view
@login_required
def fees_list(request):
    fees_records = FeesHistory.objects.all()
    return render(request, 'school_app/fees_list.html', {'fees_records': fees_records})

# Add fees record view (admin and staff only)
@login_required
def add_fees_record(request):
    if request.user.role not in ['admin', 'staff']:
        messages.warning(request, "You do not have permission to add fees records.")
        return redirect('school_app:dashboard')  # Include namespace here

    form = FeesHistoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Fees record added successfully.")
        return redirect('school_app:fees_list')  # Redirect to the fees list view
    
    return render(request, 'school_app/add_fees_record.html', {'form': form})






