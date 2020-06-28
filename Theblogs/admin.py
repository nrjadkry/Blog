from django.contrib import admin
from .models import Categories, Post, UserProfile
from import_export.admin import ImportExportModelAdmin

# admin.site.register(Categories)
# admin.site.register(Post)
admin.site.register(UserProfile)


@admin.register(Post)
class ViewAdmin(ImportExportModelAdmin):
	pass

@admin.register(Categories)
class ViewAdmin(ImportExportModelAdmin):
	list_display=('id','name')