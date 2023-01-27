
from django.contrib import admin
from django.urls import include, path

from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

# urls
urlpatterns = [
        # url(r'^$', schema_view),
    #path('docs/', schema_view),  # <-- Here
    path('api/v1/transformer', include('transformer.urls')),
    path('api/v1/movies/', include('movies.urls')),
    path('api/v1/auth/', include('authentication.urls')),
    path('admin/', admin.site.urls),
]