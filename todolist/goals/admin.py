from django.contrib import admin

from goals.models import GoalCategory, Board


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user", "board")


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Board)