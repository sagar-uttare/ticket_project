from django.contrib import admin
from .models import Ticket, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Show 1 extra comment field in the ticket view

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'assigned_engineer', 'status', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'assigned_engineer')
    inlines = [CommentInline]

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Comment)
