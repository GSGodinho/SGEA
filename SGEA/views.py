from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django import forms
from django.contrib.auth import login
from .forms import SessaoForm,CronogramaForm,EventoForm,AlunoForm,VisitanteForm,LoginForm,PalestraForm,userForm,userExternoForm
from .models import Evento,Sessao_Participante,Sessao,Cronograma
from django.contrib.auth.decorators import login_required
import datetime
from .input import EventoInsert,VisitanteInsert,Autenticacao,PalestraInsert,Dicionario_de_cronograma,Dicionario_de_Sessao
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode 



def entrada(request):
    Lista_Eventos=Evento.objects.prefetch_related('cronogramas').order_by("-id")

    Tipo=request.GET.get('tipo')
    Curso=request.GET.get('curso')
    if Tipo:
        Lista_Eventos=Lista_Eventos.filter(tipo=Tipo)
    if Curso:
        Lista_Eventos=Lista_Eventos.filter(curso=Curso)

    

    context={
        "Lista_Eventos": Lista_Eventos,
        "Filtros":[Tipo,Curso]
    }

    return render(request,'Palestra/entrada.html',context)

@login_required()
def createEvento(request,uidb64):
    Sessaoform_factory=forms.formset_factory(SessaoForm,extra=1)
    Cronogramaform_factory=forms.formset_factory(CronogramaForm,extra=1)

    if request.method == 'POST':
        #Enviando para salvar
        Eventoform=EventoForm(request.POST)
        Sessaoform=Sessaoform_factory(request.POST,prefix="sessoes")
        Cronogramaform=Cronogramaform_factory(request.POST,prefix="cronograma")
        
        if all([Eventoform.is_valid(),Cronogramaform.is_valid(),Sessaoform.is_valid()]):
            evento:Evento=Eventoform.save()
            EventoInsert(evento,Cronogramaform.cleaned_data,Sessaoform.cleaned_data)
            return redirect('Entrada')
        else:
            messages.add_message(request,messages.ERROR,Eventoform.errors)
            messages.add_message(request,messages.ERROR,Cronogramaform.errors)
            messages.add_message(request,messages.ERROR,Sessaoform.errors)
  
    else:
        #em caso de Update inserindo dados
        try:
            evento_id=urlsafe_base64_decode(uidb64)
            evento = Evento.objects.get(id=evento_id)
            Eventoform=EventoForm()
            Eventoform.initialUpdate(evento)
            
            Sessaoform=Sessaoform_factory(initial=Dicionario_de_Sessao(evento),prefix="sessoes")
            Cronogramaform=Cronogramaform_factory(initial=Dicionario_de_cronograma(evento),prefix="cronograma")
        #Criação de Novo
        except Evento.DoesNotExist:
            Eventoform=EventoForm()
            Sessaoform=Sessaoform_factory(prefix="sessoes")
            Cronogramaform=Cronogramaform_factory(prefix="cronograma")

    Mensagens= messages.get_messages(request)

    return render(request,"Palestra/formevento.html",
                  {'Eventoform':Eventoform,
                   'Sessaoform':Sessaoform,
                   'messages':Mensagens,
                   'Cronogramaform':Cronogramaform,
                   })

@login_required()   
def createPalestra(request,uidb64):
    Cronogramaform_factory=forms.formset_factory(CronogramaForm)
    
    if request.method == 'POST':
        
        Palestraform=PalestraForm(request.POST)
        Cronogramaform=Cronogramaform_factory(request.POST,prefix="cronograma")
        
        if all([Palestraform.is_valid(),Cronogramaform.is_valid()]):
            PalestraInsert(Palestraform.cleaned_data,Cronogramaform.cleaned_data)
            return redirect('Entrada')
        else:
            messages.add_message(request,messages.ERROR,Palestraform.errors)
            messages.add_message(request,messages.ERROR,Cronogramaform.errors)
  
    else:
        try:
            Cronogramaform_factory=forms.formset_factory(CronogramaForm,extra=0)
            evento_id=urlsafe_base64_decode(uidb64)
            evento = Evento.objects.get(id=evento_id)
            
            Palestraform=PalestraForm()
            Palestraform.initialUpdate(evento)
            Cronogramaform=Cronogramaform_factory(initial=Dicionario_de_cronograma(evento),prefix="cronograma")
            
        except Evento.DoesNotExist:
            Palestraform=PalestraForm()
            Cronogramaform=Cronogramaform_factory(prefix="cronograma")

    Mensagens= messages.get_messages(request)

    return render(request,"Palestra/formpalestra.html",
                  {'Palestraform':Palestraform,
                   'messages':Mensagens,
                   'Cronogramaform':Cronogramaform,
                   })

def detalhes(request,uidb64):
    try:
        evento_id=urlsafe_base64_decode(uidb64)
        evento=Evento.objects.get(id=evento_id)
        cronogramas=Cronograma.objects.filter(evento=evento).order_by('data_hora_inicio')
        sessoes= Sessao.objects.filter(cronograma__in=cronogramas).order_by('cronograma__data_hora_inicio')
        cronogramas=cronogramas.exclude(id__in=sessoes.values_list("cronograma_id")).order_by('data_hora_inicio')
        
        context ={
            "Evento":evento,
            "Cronogramas":cronogramas,
            "Sessoes":sessoes
        }
        return render(request,"Palestra/details.html",context)
    except Exception as e:
        return HttpResponse(str(e))
   
def CadastroVisitante(request):
    if request.method == 'POST':
        visitanteform=VisitanteForm(request.POST)
        if (visitanteform.is_valid()):
            user=VisitanteInsert(visitanteform.cleaned_data)
            login(request,user)
            return redirect('Entrada')
        else:
            messages.add_message(request,messages.ERROR,visitanteform.errors)
    else:
        visitanteform=VisitanteForm()
    Mensagens= messages.get_messages(request)
    return render(request,"Usuario/CadastroVisitante.html",
                    {'visitanteform':visitanteform,
                     'messages':Mensagens
                    })

def CadastroAluno(request):
    if request.method == 'POST':
        alunoform=AlunoForm()
        if (alunoform.is_valid()):
            """user=AlunoInsert(alunoform.cleaned_data)
            login(request,user)"""""
        else:
            messages.add_message(request,messages.ERROR,alunoform.errors)
    else:
        alunoform=AlunoForm()
    Mensagens= messages.get_messages(request)
    return render(request,"Usuario/CadastroAluno.html",
                    {'alunoform':alunoform,
                     'messages':Mensagens
                    })

def usuariologin(request):
    if request.method=='POST':
        loginform= LoginForm(request.POST)
        
        if(loginform.is_valid() and Autenticacao(loginform.cleaned_data,request)):
            return redirect('Entrada')       
        else:
            loginform.add_error(None, 'Credenciais inválidas.')
    else:
        loginform= LoginForm()

    Mensagens= messages.get_messages(request)
    return render(request,"Usuario/login.html",
                    {'loginform':loginform,
                    })

@login_required()
def usuarioDetalhes(request):
    #try:
        userform=userForm(instance=request.user)
        externoform= userExternoForm(instance=request.user.participanteEX)

        if request.user.is_authenticated and request.method=='POST':

            userform = userForm(request.POST,instance=request.user)
            externoform= userExternoForm(request.POST,instance=request.user.participante)

            if all([userform.is_valid(),externoform.is_valid()]):
                userform.save()
                externoform.save()
            else:
                messages.add_message(request,messages.ERROR,userform.errors)
                messages.add_message(request,messages.ERROR,externoform.errors)
        
        Mensagens= messages.get_messages(request)
        return render(request,"Usuario/Usuario.html",{"userform":userform,
                                                    "externoform":externoform,
                                                    "messages":Mensagens})
    #except :
        return redirect('Entrada')

@login_required()
def inscrito(request):
    try:
        sessao_participante=Sessao_Participante.objects.filter(participante=request.user).select_related("Sessao__cronograma__evento")

        context={
            "SessaoParticipante":sessao_participante
        }
        return render(request,'Palestra/Inscricoes.html',context)
    except:
       return redirect('Entrada')

@login_required()  
def deleteEvento(request,uidb64):
    if request.method == 'POST':
        loginform= LoginForm(request.POST)
        if(loginform.is_valid() and Autenticacao(loginform.cleaned_data,request) and request.user.is_superuser):
            evento_id=urlsafe_base64_decode(uidb64)
            evento = get_object_or_404(Evento,id=evento_id)
            evento.delete()
            return redirect('Entrada')
        else:
            loginform.add_error(None, 'Credenciais inválidas.')
    else:
        loginform= LoginForm()

    Mensagens= messages.get_messages(request)
    return render(request,"Palestra/Delete.html",
                    {'loginform':loginform,
                    })

        




