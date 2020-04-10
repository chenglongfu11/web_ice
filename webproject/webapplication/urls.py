from django.urls import path

from . import views

app_name = 'webapplication'
urlpatterns = [
    #ex: /
    path('', views.index, name='index'),
    # ex: /webapplication/5/
    # path('<int:pk>/', views.detail, name='detail'),
    #detail(request=<HttpRequest object>, question_id=34)
    # ex: /webapplication/5/results/
    # path('<int:pk>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path('functions/', views.function_list, name='function_list'),
    path('functions/1/', views.addfloor, name ='addfloor'),
    path('functions/showall/', views.showAll, name='showAllthing'),
    path('graphs/building52/',views.building52, name='building52'),
    path('wwr/', views.wwr),
]

