
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('admin/', admin.site.urls),

    path('admin/d/h/v/d/u/g/o/d/h/e/l/p/m/e/a/l/w/a/y/s/a/m/e/n', admin.site.urls),
    path('',include('accounts.urls')),
   # path('',include('financee.urls')),
    path('',include('mails.urls')),
    path('',include('incomestatement.urls')),
    path('',include('sms.urls')),
    path('',include('fees.urls')),

]
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
 