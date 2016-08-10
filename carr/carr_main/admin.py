from django.contrib import admin
from pagetree.models import SectionChildren, PageBlock

from carr.carr_main.models import SiteState
from models import Section
from models import SiteSection


class SectionChildrenInline(admin.StackedInline):
    model = SectionChildren
    fk_name = 'parent'
    extra = 0
    fields = ('child',)
    template = 'admin/pagetree/sectionchildren/edit_inline/stacked.html'


class PageBlockInline(admin.StackedInline):
    model = PageBlock
    extra = 0
    fields = ('label', )
    template = 'admin/pagetree/pageblock/edit_inline/stacked.html'


class SectionAdmin(admin.ModelAdmin):
    list_display = ('label', 'slug')
    fields = ('label', 'slug', 'sites')

    inlines = [
        SectionChildrenInline,
        PageBlockInline,
    ]

admin.site.unregister(Section)
admin.site.register(SiteSection, SectionAdmin)


class SiteStateAdmin(admin.ModelAdmin):
    list_display = ['user', 'last_location']
    search_fields = ['user__username']

admin.site.register(SiteState, SiteStateAdmin)
