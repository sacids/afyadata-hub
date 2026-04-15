from django.contrib import admin
from django.utils.html import format_html
from .models import AuthorizedInstance, PublicProject

# This allows you to view and edit projects directly from the Instance page
class PublicProjectInline(admin.TabularInline):
    model = PublicProject
    extra = 0
    readonly_fields = ('project_code',)
    fields = ('title', 'project_code', 'instance_url', 'is_active')

@admin.register(AuthorizedInstance)
class AuthorizedInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_api_key', 'project_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'api_key')
    inlines = [PublicProjectInline]
    actions = ['deactivate_instances', 'activate_instances']

    # Custom Column: Display the API Key in a code block for easy copying
    def display_api_key(self, obj):
        return format_html(
            '<code style="background: #eee; padding: 2px 5px; border-radius: 4px;">{}</code>',
            obj.api_key
        )
    display_api_key.short_description = 'API Key'

    # Custom Column: Show count of projects for this instance
    def project_count(self, obj):
        count = obj.projects.count()
        return format_html('<b>{}</b>', count)
    project_count.short_description = 'Projects'

    # Bulk Actions
    @admin.action(description="Deactivate selected instances")
    def deactivate_instances(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Activate selected instances")
    def activate_instances(self, request, queryset):
        queryset.update(is_active=True)

@admin.register(PublicProject)
class PublicProjectAdmin(admin.ModelAdmin):
    list_display = ('project_code', 'title', 'get_instance_name', 'instance_url', 'is_active', 'created_at')
    list_filter = ('is_active', 'registered_by', 'created_at')
    search_fields = ('title', 'project_code', 'instance_url')
    readonly_fields = ('project_code', 'registered_by')
    
    # Organize fields into sections (Fieldsets)
    fieldsets = (
        ('Identification', {
            'fields': ('project_code', 'title', 'description')
        }),
        ('Technical Routing', {
            'fields': ('registered_by', 'instance_url', 'remote_project_id')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def get_instance_name(self, obj):
        return obj.registered_by.name
    get_instance_name.short_description = 'Hosting Instance'