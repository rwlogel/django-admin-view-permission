from __future__ import unicode_literals

from django.contrib import admin
from parler.admin import TranslatableAdmin

from admin_view_permission import admin as view_admin

from .models import *  # noqa: F403


# Modeladmin for the UI
class StackedModelAdmin(admin.StackedInline):
    model = TestModel2


class TabularModelAdmin(admin.TabularInline):
    model = TestModel3


class DefaultModelAdmin(admin.ModelAdmin):
    inlines = [
        StackedModelAdmin,
        TabularModelAdmin
    ]

    def has_delete_permission(self, request, obj=None):
        if not super(DefaultModelAdmin, self).has_delete_permission(
            request, obj
        ):
            return False

        # Don't allow objects where var1 is 'protected' to be deleted
        if obj:
            return obj.var1 != 'protected'
        elif (
            request.POST and
            request.POST.get('action') == 'delete_selected' and
            request.path.startswith('/admin/test_app/testmodel1/')
        ):
            # Bulk delete
            ids = request.POST.getlist(admin.helpers.ACTION_CHECKBOX_NAME)
            return not (
                TestModel1.objects
                .filter(id__in=ids, var1='protected')
                .exists()
            )

        return True

    def other_action(self, request, queryset):
        return Http

    other_action.description = 'Other Action'

    actions = [other_action]


admin.site.register(TestModel1, DefaultModelAdmin)


class TestModelParlerAdmin(TranslatableAdmin, admin.ModelAdmin):
    model = TestModelParler


admin.site.register(TestModelParler, TestModelParlerAdmin)


# Modeladmin for testing
class StackedModelAdmin1(admin.StackedInline):
    model = TestModel4


class TabularModelAdmin2(admin.TabularInline):
    model = TestModel6


class ModelAdmin1(view_admin.AdminViewPermissionModelAdmin):
    inlines = [
        StackedModelAdmin1,
        TabularModelAdmin2,
    ]

    def other_action(self, request, queryset):
        pass
    other_action.description = 'Other Action'

    actions = [other_action]
