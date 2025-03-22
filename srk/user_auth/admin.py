from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ReportIssue

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'full_name', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'full_name', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

from .models import ReportIssue
@admin.register(ReportIssue)
class ReportIssueAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_no', 'issue_description', 'latitude', 'longitude', 'submitted_at')
    search_fields = ('user__username', 'contact_no', 'issue_description')


from .models import Admin

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'application_id', 'email', 'post', 'posted_area','profile_picture')
    search_fields = ('full_name', 'email', 'application_id')


from .models import ProjectDetail

@admin.register(ProjectDetail)
class ProjectDetailAdmin(admin.ModelAdmin):
    list_display = ('work', 'location', 'start_date', 'status', 'fund_granted')
    search_fields = ('work', 'location')
    list_filter = ('status', 'start_date')
