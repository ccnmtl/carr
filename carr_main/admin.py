from django.contrib import admin
from models import SiteSection
from models import Section
from pagetree.models import Hierarchy, SectionChildren, PageBlock
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld


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

#import pdb
#pdb.set_trace()

class SectionAdmin(admin.ModelAdmin):
    list_display = ('label', 'slug', 'template')
    fields = ('label', 'slug', 'template', 'sites')

    inlines = [ 
            SectionChildrenInline,
            PageBlockInline,
        ]

admin.site.unregister(Section)
admin.site.register(SiteSection, SectionAdmin)




print "AAAAAAA"
class FlatPageAdmin(FlatPageAdminOld):
    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)

# We have to unregister it, and then reregister
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

