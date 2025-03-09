from django.contrib import admin
from .models import User, SurveyQuestion, SurveyCategory

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "선택한 사용자를 승인하였습니다.")
    approve_users.short_description = "선택한 사용자 승인"

class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ('text_en', 'text_ko', 'category')
    list_filter = ('category',)
    search_fields = ('text_en', 'text_ko')
    fieldsets = (
        ('질문 내용', {
            'fields': ('text_en', 'text_ko', 'category')
        }),
        ('Never/전혀 그렇지 않다', {
            'fields': ('weight_never_en', 'weight_never_ko', 'weight_never_value')
        }),
        ('Sometimes/가끔 그렇다', {
            'fields': ('weight_sometimes_en', 'weight_sometimes_ko', 'weight_sometimes_value')
        }),
        ('Often/자주 그렇다', {
            'fields': ('weight_often_en', 'weight_often_ko', 'weight_often_value')
        }),
        ('Always/항상 그렇다', {
            'fields': ('weight_always_en', 'weight_always_ko', 'weight_always_value')
        }),
    )

@admin.register(SurveyCategory)
class SurveyCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'title_en', 'title_ko')
    search_fields = ('code', 'title_en', 'title_ko')
    ordering = ('code',)

admin.site.register(User, UserAdmin)
admin.site.register(SurveyQuestion, SurveyQuestionAdmin)
# admin.site.register(SurveyCategory, SurveyCategoryAdmin)
