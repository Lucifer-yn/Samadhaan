from django.shortcuts import render,HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReportIssueForm
from django.contrib.auth import authenticate, login, logout

# Get the custom user model
# Get the custom user model
# Get the custom user model
CustomUser = get_user_model()

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required!")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        # Create user
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Authenticate and log in the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Set session to expire when the browser closes
            request.session.set_expiry(0)
            messages.success(request, "Registration successful! Redirecting to report page.")
            return redirect('report')  # Redirect to report page
        
        messages.error(request, "Something went wrong. Please try again.")
        return redirect('register')

    return render(request, "register.html")

# Create your views here.
def index(request):
    return HttpResponse(request,"hello world")

def home(request):
    return render(request,"home.html")

def diversity(request):
    return render(request,"diversity.html")

def fields(request):
    return render(request,"fields.html")

from .models import ProjectDetail
def ad_info(request):
    projects = ProjectDetail.objects.all()  # Fetch all projects from the database
    return render(request, 'ad_info.html', {'projects': projects})

from .models import ReportIssue
from .forms import ReportIssueForm
@login_required(login_url='register')  # Requires login
def report(request): 
    states = {
        "Andhra Pradesh": ["Anantapur", "Chittoor", "Guntur"],
        "Bihar": ["Araria", "Patna", "Gaya"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
        "Madhya Pradesh": ["Bhopal", "Indore", "Raisen"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    }

    sorted_states = dict(sorted(states.items()))  
    for state in sorted_states:
        sorted_states[state] = sorted(sorted_states[state])

    if request.method == "POST":
        form = ReportIssueForm(request.POST, request.FILES)
        print("Form Data:", request.POST)  # Debugging print statement

        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user  # Assign the current logged-in user
            report.save()
            print("Report Saved Successfully!")  # Debugging print statement
            messages.success(request, "Your report has been submitted successfully.")
            return redirect('home')
        else:
            print("Form Errors:", form.errors)  # Debugging print statement
            messages.error(request, "There was an error in your submission.")

    else:
        form = ReportIssueForm()

    return render(request, "report.html", {'form': form, 'states': sorted_states})



def auto_logout(request):
    logout(request)
    return redirect('register') 


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AdminRegistrationForm
from .models import Admin,ProjectDetail
from django.contrib.auth import login

def admin_login_view(request):
    if request.method == "POST":
        application_id = request.POST.get('application_id')  # Get application ID
        password = request.POST.get('password')

        if not application_id or not password:
            messages.error(request, "Both Application ID and Password are required!")
            return redirect('admin_login')

        try:
            admin_user = Admin.objects.get(application_id=application_id)

            # Check the password manually
            if admin_user.check_password(password):  # Ensure password is hashed
                request.session['admin_id'] = admin_user.id  # Store admin session
                request.session['is_admin_logged_in'] = True  # Add an extra session flag

                messages.success(request, "Login successful!")
                return redirect('admin_dashboard')  # Redirect to admin dashboard

            else:
                messages.error(request, "Invalid credentials!")

        except Admin.DoesNotExist:
            messages.error(request, "Admin not found!")

    return render(request, "admin_login.html")

# Admin Registration (if needed)
def admin_register(request):
    if request.method == 'POST':
        print(request.POST)  # Debugging statement

        full_name = request.POST.get('full_name', '').strip()
        application_id = request.POST.get('application_id', '').strip()
        email = request.POST.get('email', '').strip()
        post = request.POST.get('post', '').strip()
        posted_area = request.POST.get('posted_area', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        profile_picture = request.FILES.get('profile_picture')

        # Check if any field is empty
        if not all([full_name, application_id, email, post, posted_area, password, confirm_password]):
            messages.error(request, "All fields are required!")
            return redirect('admin_register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('admin_register')

        admin_user = Admin.objects.create(
            full_name=full_name,
            application_id=application_id,
            email=email,
            post=post,
            posted_area=posted_area,
            profile_picture=profile_picture
        )
        admin_user.set_password(password)
        admin_user.save()

        messages.success(request, "Admin registered successfully!")
        return redirect('admin_login')

    return render(request, 'admin_register.html')

# Admin Dashboard View
from django.conf import settings 

def admin_dashboard(request):
    # Ensure the admin is logged in
    admin_id = request.session.get('admin_id')
    
    if not admin_id:
        messages.error(request, "You must be logged in as an admin.")
        return redirect('admin_login')  

    try:
        admin_user = Admin.objects.get(id=admin_id) 
    except Admin.DoesNotExist:
        messages.error(request, "Admin account not found.")
        return redirect('admin_login')  

    # Check if the profile picture exists; otherwise, use a default image
    profile_picture_url = admin_user.profile_picture.url if admin_user.profile_picture else settings.STATIC_URL + "default_profile.jpg"

    projects = ProjectDetail.objects.all()  

    context = {
        'admin_user': admin_user, 
        'profile_picture_url': profile_picture_url,  
        'projects': projects,  
    }

    return render(request, "admin_dashboard.html", context)

# Project Detail View
@login_required(login_url='admin_login')
def project_detail(request):
    if request.method == "POST":
        location = request.POST.get("location")
        work = request.POST.get("work")
        start_date = request.POST.get("start_date")
        completion_date = request.POST.get("completion_date")
        status = request.POST.get("status")
        fund_granted = request.POST.get("fund_granted")
        estimate_file = request.FILES.get("estimate_file")
        site_image = request.FILES.get("site_image")

        print("Location:", location)
        print("Work:", work)
        print("Start Date:", start_date)
        print("Completion Date:", completion_date)
        print("Status:", status)
        print("Fund Granted:", fund_granted)
        print("Estimate File:", estimate_file)
        print("Site Image:", site_image)

        # Save to the database
        project = ProjectDetail(
            location=location,
            work=work,
            start_date=start_date if start_date else None,  # Handle empty value
            completion_date=completion_date if completion_date else "N/A",
            status=status,
            fund_granted=fund_granted if fund_granted else None,
            estimate_file=estimate_file if estimate_file else None,
            site_image=site_image if site_image else None
        )
        project.save()

        return redirect("admin_dashboard")  # Redirect after saving
    return render(request, "project_detail.html")

# Admin Logout
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('admin_login')

from django.shortcuts import render, redirect, get_object_or_404
def edit_project(request, project_id):
    project = get_object_or_404(ProjectDetail, id=project_id)

    if request.method == "POST":
        project.location = request.POST.get("location")
        project.work = request.POST.get("work")
        project.start_date = request.POST.get("start_date") or project.start_date
        project.completion_date = request.POST.get("completion_date") or project.completion_date
        project.status = request.POST.get("status")
        project.fund_granted = request.POST.get("fund_granted") or project.fund_granted

        if "estimate_file" in request.FILES:
            project.estimate_file = request.FILES["estimate_file"]

        if "site_image" in request.FILES:
            project.site_image = request.FILES["site_image"]

        project.save()
        return redirect("admin_dashboard")

    return render(request, "edit_project.html", {"project": project})

def delete_project(request, project_id):
    project = get_object_or_404(ProjectDetail, id=project_id)
    project.delete()
    return redirect("admin_dashboard")
