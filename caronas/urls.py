from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_caronas, name='registrar_caronas'),
    path('cadastrar-passageiro/', views.cadastrar_passageiro, name='cadastrar_passageiro'),
    path('dia/', views.visualizar_dia, name='visualizar_dia'),
    path('carona/editar/<int:pk>/', views.editar_carona, name='editar_carona'),
    path('carona/deletar/<int:pk>/', views.deletar_carona, name='deletar_carona'),
    path('fechar-conta/', views.fechar_conta, name='fechar_conta'),
    path('fechar-conta/pdf/<int:passageiro_id>/', views.gerar_pdf_cobranca, name='gerar_pdf_cobranca'),
]