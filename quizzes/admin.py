from django.contrib import admin
from .models import Quiz, Question


class QuestionInline(admin.TabularInline):
    """Inline admin interface for Question model within QuizAdmin."""
    model = Question
    extra = 1
    fields = ['question_title', 'question_options', 'answer']
    max_num = 10
    min_num = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin interface for Quiz model."""
    list_display = ['id', 'title', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [QuestionInline]

    fieldsets = (
        ('Quiz Information', {
            'fields': ('user', 'title', 'description', 'video_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Question model."""
    list_display = ['id', 'question_title', 'quiz', 'created_at']
    list_filter = ['created_at', 'quiz']
    search_fields = ['question_title', 'answer']
    readonly_fields = ['created_at', 'updated_at']