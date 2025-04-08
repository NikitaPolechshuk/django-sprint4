from django.conf import settings
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf.urls.static import static
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from pages import views

handler404 = 'pages.views.handler_404'
handler500 = 'pages.views.handler_500'

urlpatterns = [
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/logout',
         views.user_logout,
         name='logout'),
    path('auth/registration/success',
         views.RegistrationSuccessPage.as_view(),
         name='registration_success'),
    path('auth/registration/',
         CreateView.as_view(
             template_name='registration/registration_form.html',
             form_class=UserCreationForm,
             success_url=reverse_lazy('registration_success'),
         ),
         name='registration'),
]

# if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
