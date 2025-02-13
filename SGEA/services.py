from django.shortcuts import redirect,get_object_or_404,render,reverse
from .models import Evento,Sessao,Cronograma,Sessao_Participante
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
import segno

@login_required
def inscrever(request, uidb64): 
    try:
        if request.user.is_authenticated:
            evento_id=urlsafe_base64_decode(uidb64)
            evento = get_object_or_404(Evento,id=evento_id)
            cronogramas = Cronograma.objects.filter(evento=evento)
            sessoes= Sessao.objects.filter(cronograma__in=cronogramas)
            sessao_count= Sessao_Participante.objects.filter(Sessao__in=sessoes).filter(participante=request.user).count()
            if sessao_count<sessoes.count():
                for sessao in sessoes:
                    sessao_participante=Sessao_Participante.objects.create(Sessao=sessao,participante=request.user)
                return redirect('Entrada')
            else:
                return render(request,"Palestra/Inscrito.html",{"Evento": evento})
    except Exception as e:
        return HttpResponse(content="Error"+e)
    
def qr_codePresenca(request,uidb64):

    response=qrcode(reverse("Presenca",args=[uidb64]))
    return response

def qrcode(data):
    # Gera o QR code usando o Segno
    qr = segno.make(data,micro=False)

    # Cria uma resposta HTTP com o tipo de conteúdo 'image/png'
    response = HttpResponse(content_type='image/png')
    
    # Salva a imagem do QR code diretamente na resposta
    qr.save(response, kind='png',scale=10)

    # Retorna a resposta com a imagem do QR code
    return response

def Presenca(request,uidb64):
    try:
        if request.user.is_authenticated:
            evento_id=urlsafe_base64_decode(uidb64)
            evento = get_object_or_404(Evento,id=evento_id)
            cronogramas=Cronograma.objects.filter(evento=evento.id)
            sessoes= Sessao.objects.filter(cronograma__in=cronogramas)

            sessao_participante=Sessao_Participante.objects.filter(Sessao__in=sessoes,participante=request.user)
            sessao_participante=sessao_participante.update(confirmacao=True)

            return HttpResponse(content="inscrito")
        else:
            return HttpResponse(content="Usuario não valido")
    except Exception as e:
        return HttpResponse(content="Error"+str(e))
    

    
        
    