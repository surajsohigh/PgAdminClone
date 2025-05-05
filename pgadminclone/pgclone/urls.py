from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('listtable', list_tables),
    path("tables/<str:table_name>", get_table_data),
    path("query", execute_query),
    path("columns/<str:table_name>/", get_table_columns)


    


    
]
