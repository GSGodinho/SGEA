from django.urls import path
from django.contrib.auth import views as auth_views

from . import views,services

urlpatterns = [
    path("", views.entrada, name="Entrada"),

    path("detalhes/<uidb64>",views.detalhes,name="detalhes"),

    path("create/Evento/<uidb64>",views.createEvento,name="Evento"),
    path("create/Palestra/<uidb64>",views.createPalestra,name="Palestra"),
    path("cadastro/Aluno",views.CadastroAluno,name="CadastroAluno"),
    path("cadastro/Visitante",views.CadastroVisitante,name="CadastroVisitante"),
    
    path("inscrever/<uidb64>/",services.inscrever,name="Inscrever"),
    path("login/",views.usuariologin,name="login"),
    path("usuario/detalhes",views.usuarioDetalhes,name="usuarioDetalhes"),
    path("inscricoes",views.inscrito,name='inscricoes'),
    
    path('recuperacaoSenha/pedido', auth_views.PasswordResetView.as_view(template_name='Usuario/RecuperacaoSenha/Pedido.html'), name='password_reset'),
    path('recuperacaoSenha/enviado', auth_views.PasswordResetDoneView.as_view(template_name='Usuario/RecuperacaoSenha/Enviado.html'), name='password_reset_done'),
    path('recuperacaoSenha/principal/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Usuario/RecuperacaoSenha/Principal.html'), name='password_reset_confirm'),
    path('recuperacaoSenha/concluido/', auth_views.PasswordResetCompleteView.as_view(template_name='Usuario/RecuperacaoSenha/Concluido.html'), name='password_reset_complete'),
    path('qrcode/<uidb64>',services.qr_codePresenca,name='qrCode'),
    path('Presenca/<uidb64>',services.Presenca,name='Presenca')

    
    path('Delete/<uidb64>',views.deleteEvento,name='Delete')
]