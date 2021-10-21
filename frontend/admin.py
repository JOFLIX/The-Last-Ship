from django.contrib import admin
from .models import IndexPage,AboutPage,NewsEvents,MessagesFromVisitors,Contacts,Alumni,Accreditation,Admission
# Register your models here.
admin.site.register(IndexPage)
admin.site.register(AboutPage)
admin.site.register(NewsEvents)
admin.site.register(MessagesFromVisitors)
admin.site.register(Contacts)
admin.site.register(Accreditation)
admin.site.register(Admission)
admin.site.register(Alumni)