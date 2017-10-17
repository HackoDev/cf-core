from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.utils.translation import ugettext_lazy as _
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from .models import (
    ModerationNote, SliderImage, SocialLink, InformationPartner,
    RegularPartner, Location, Contact, Status, ServiceRule, Location
)


class BaseModerationModelAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        readonly_fiels = super(BaseModerationModelAdmin, self).\
            get_readonly_fields(request, obj=obj)
        return readonly_fiels + ('is_available', 'approved_by', 'approved_at')


    def save_formset(self, request, form, formset, change):
        for form in formset:
            if isinstance(form.instance, ModerationNote):
                if form.instance._state.adding:
                    form.instance.created_by = request.user
        formset.save()


class BaseSortableAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


class BasePartnerAdmin(BaseSortableAdmin):

    exclude = ('base_type',)


class RuleInline(SortableInlineAdminMixin, admin.TabularInline):

    model = ServiceRule
    extra = 0


class RuleAdmin(BaseSortableAdmin):

    fields = ('text', )

    def get_queryset(self, request):
        return super(RuleAdmin, self).get_queryset(request).filter(parent=None)

    inlines = [
        RuleInline
    ]


class SocialLinkAdmin(BaseSortableAdmin):
    list_filter = ('id', 'name', 'url')


class ModerationNoteInLine(admin.StackedInline, GenericStackedInline):

    readonly_fields = ('last_seen', 'created', 'created')
    model = ModerationNote
    extra = 0


admin.site.site_header = _("Crowd funding administrate")
admin.site.site_title = _("Crowd funding administrate")
admin.site.index_title = _("Crowd funding")


admin.site.register(RegularPartner, BasePartnerAdmin)
admin.site.register(InformationPartner, BasePartnerAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)
admin.site.register(Location, BaseSortableAdmin)
admin.site.register(ServiceRule, RuleAdmin)
admin.site.register(Contact, BaseSortableAdmin)
admin.site.register(SliderImage, BaseSortableAdmin)
admin.site.register(Status, BaseSortableAdmin)
