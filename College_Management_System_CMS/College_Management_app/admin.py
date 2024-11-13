from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import C_User, AdminHOD, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, LeaveReportStaff, FeedBackStudent, FeedBackStaffs, NotificationStudent, NotificationStaffs, SessionYearModel

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(C_User, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackStaffs)
admin.site.register(NotificationStudent)
admin.site.register(NotificationStaffs)
admin.site.register(SessionYearModel)
class SessionYearModelAdmin(admin.ModelAdmin):
    list_display = ('start_year', 'end_year')
