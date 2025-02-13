from .models import Evento,Cronograma,Palestrante,Sessao,Participante,Participante_Externo
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from datetime import datetime

def EventoInsert(EventoNovo,CronogramaInsert,SessaoInsert):
    """
    tipo="Evento"

    EventoNovo,eventoCreated= Evento.objects.update_or_create(
                    id=EventoInsert['id'],
                    defaults={
                        "titulo": EventoInsert['titulo'],
                        "dt_inicio" :EventoInsert['dt_inicio'],
                        "dt_fim" :EventoInsert['dt_fim'],
                        "tema" :EventoInsert['tema'],
                        "descricao" : EventoInsert['descricao'],
                        "dt_inicio_inscricao" : EventoInsert['dt_inicio_inscricao'],
                        "dt_fim_inscricao" :EventoInsert['dt_fim_inscricao'],
                        "perc_necess_cert" :EventoInsert['perc_necess_cert'],
                        "cert_por_palestra" :EventoInsert['cert_por_palestra'],
                        "tipo" :tipo,
                        "limite_inscricao" :EventoInsert['limite_inscricao'],
                        "curso" :EventoInsert['curso']
                    }
                    
        )
    """
    
    sessoes=[]
    cronogramas=[]
    palestrantes=[]
    for cronograma in CronogramaInsert:
        if cronograma:
            CronogramaNovo,cronogramaCreated= Cronograma.objects.update_or_create(
                id=cronograma['id'],
                defaults={
                    "assunto": cronograma['Assunto'],
                    "local":cronograma['local'],
                    "data_hora_inicio":cronograma['DT_Hora_inicio'],
                    "data_hora_fim":cronograma['DT_Hora_fim'],
                    "evento": EventoNovo
                }
            )
            cronogramas.append(CronogramaNovo.id)
    
    for sessao in SessaoInsert:
        if sessao:
            CronogramaSessao,cronogramaSessaoCreated=Cronograma.objects.update_or_create(
                id=sessao['id_cronograma'],
                defaults={
                    "assunto": sessao['titulo'],
                    "local":sessao['local'],
                    "data_hora_inicio":sessao['DT_Hora_inicio'],
                    "data_hora_fim":sessao['DT_Hora_fim'],
                    "evento": EventoNovo
                }
            )
            cronogramas.append(CronogramaSessao.id)
            
            PalestranteSessao,palestranteCreated= Palestrante.objects.update_or_create(
                id=sessao['id_palestrante'],
                defaults=
                {
                    "nome":sessao['NomePalestrante'],
                    "curriculo":sessao['NomePalestrante']
                }
            )
            palestrantes.append(PalestranteSessao.id)
            
            
            SessaoNovo,sessaoCreated= Sessao.objects.update_or_create(
                id=sessao['id'],
                defaults={
                    "titulo":sessao['titulo'],
                    "descricao": sessao['descricao'],
                    "cronograma":CronogramaSessao,
                    "palestrante":PalestranteSessao
                }
            )
            sessoes.append(CronogramaNovo.id)

    #Excluir Sessões ou Cronogramas apagadas
    #filtra por cronogrmas,sessoes e palestrante do evento, remove dessa coleta aqueles criados ou modificados em Update
    cronogramasFiltro = Cronograma.objects.filter(evento=EventoNovo).exclude(id__in=cronogramas)
    sessoesFiltros= Sessao.objects.filter(cronograma__in=cronogramasFiltro).exclude(id__in=sessoes)
    palestrantesFiltros=Palestrante.objects.filter(id__in=sessoesFiltros).exclude(id__in=palestrantes)
    
    cronogramasFiltro.delete()
    sessoesFiltros.delete()
    palestrantesFiltros.delete()
    
def PalestraInsert(PalestraInsert,CronogramaInsert):
    try:
        cronogramas = []
        
        tipo="Palestra"
        perc_necess_cert=100
        cert_por_palestra=False
        data=PalestraInsert['data']
        hora_inicio= PalestraInsert['hora_inicio']
        hora_fim= PalestraInsert['hora_fim']
        dt_inicio= datetime.combine(data,hora_inicio)
        dt_fim= datetime.combine(data,hora_fim)

        palestraNovo,palestraCreated= Evento.objects.update_or_create(
                        id=PalestraInsert['id'],
                        defaults={
                            "titulo":PalestraInsert['titulo'],
                            "dt_inicio":dt_inicio,
                            "dt_fim":dt_fim,
                            "tema":PalestraInsert['tema'],
                            "descricao": PalestraInsert['descricao'],
                            "dt_inicio_inscricao": PalestraInsert['dt_inicio_inscricao'],
                            "dt_fim_inscricao":PalestraInsert['dt_fim_inscricao'],
                            "perc_necess_cert":perc_necess_cert,
                            "cert_por_palestra":cert_por_palestra,
                            "tipo":tipo,
                            "limite_inscricao":PalestraInsert['limite_inscricao'],
                            "curso":PalestraInsert['curso']
                        }
                        )
        
        CronogramaPalestra,cronogramaPalestraCreated=Cronograma.objects.update_or_create(
            id=PalestraInsert['id_cronograma'],
            defaults={
                "assunto": PalestraInsert['titulo'],
                "local":PalestraInsert['local'],
                "data_hora_inicio":dt_inicio,
                "data_hora_fim":dt_fim,
                "evento": palestraNovo
            }
        )
        cronogramas.append(CronogramaPalestra.id)
        
        palestrante,palestranteCreated=Palestrante.objects.update_or_create(
            id=PalestraInsert['id_palestrante'],
            defaults={
                "nome":PalestraInsert['nomePalestrante'],
                "curriculo":PalestraInsert['breve_curriculo']
            }
        )
        sessao,sessaoCreated=Sessao.objects.update_or_create(
            id=PalestraInsert['id_sessao'],
            defaults={
                "titulo":PalestraInsert['titulo'],
                "descricao": PalestraInsert['descricao'],
                "cronograma":CronogramaPalestra,
                "palestrante":palestrante
            }
        )
        
        for cronograma in CronogramaInsert:
            CronogramaNovo,cronogramaCreated= Cronograma.objects.update_or_create(
                id=cronograma['id'],
                defaults={
                    "assunto": cronograma['Assunto'],
                    "local":cronograma['local'],
                    "data_hora_inicio":cronograma['DT_Hora_inicio'],
                    "data_hora_fim":cronograma['DT_Hora_fim'],
                    "evento": palestraNovo
                }
            )
            cronogramas.append(CronogramaNovo.id)
            
        cronogramasFiltro = Cronograma.objects.filter(evento=palestraNovo).exclude(id__in=cronogramas)
        cronogramasFiltro.delete()
    except:
        raise ValidationError(
            "Erro na entrada de Dado"
        )

def Autenticacao(LoginInsert,request):
    usuario = LoginInsert['usuario']
    senha = LoginInsert['senha']
    user=authenticate(request,username=usuario,password=senha)
    if user is not None:
        login(request,user)
        return True
    else:
        return False
def VisitanteInsert(VisitanteInsert):
    user = Participante.objects.create_user(
        Nome=VisitanteInsert['nome'],
        email=VisitanteInsert['email'],
        cpf=VisitanteInsert['cpf'],
        password= VisitanteInsert['senha'],
        username=VisitanteInsert['usuario']
    )
    externo=Participante_Externo.objects.create(
        participante=user,
        telefone= VisitanteInsert['telefone'],
        instituicao=VisitanteInsert['instituicao_ensino']
    )
    return user
        
#Converte o dados do BD para os forms
def Dicionario_de_Evento(evento:Evento):
    data={
        "id":evento.id,
        "titulo":evento.titulo,
        "tema" :evento.tema,
        "descricao":evento.descricao,
        "dt_inicio":evento.dt_inicio.strftime("%Y-%m-%dT%H:%M"),
        "dt_fim":evento.dt_fim.strftime("%Y-%m-%dT%H:%M"),
        "dt_inicio_inscricao":evento.dt_inicio_inscricao.strftime("%Y-%m-%dT%H:%M"),
        "dt_fim_inscricao":evento.dt_fim_inscricao.strftime("%Y-%m-%dT%H:%M"),
        "perc_necess_cert":evento.perc_necess_cert,
        "cert_por_palestra":evento.cert_por_palestra,
        "limite_inscricao":evento.limite_inscricao,
        "curso":evento.curso,
    }
    return data
def Dicionario_de_cronograma(evento:Evento):

    cronogramas= evento.cronogramas.filter(sessoes__isnull=True) #Busca os Cronograma que não estão relacionados a nenhuma sessao
    crongrama_data= []
    for cronograma in cronogramas:
        data={
            "id":cronograma.id,
            "Assunto":cronograma.assunto,
            "local":cronograma.local,
            "DT_Hora_inicio":cronograma.data_hora_inicio.strftime("%Y-%m-%dT%H:%M"),
            "DT_Hora_fim":cronograma.data_hora_fim.strftime("%Y-%m-%dT%H:%M")
        }
        crongrama_data.append(data)
    return crongrama_data
def Dicionario_de_Sessao(evento:Evento):
    cronograma= Cronograma.objects.filter(evento_id= evento.id)
    sessoes = Sessao.objects.filter(cronograma__in=cronograma)
    sessao_data= []
    for sessao in sessoes:
        data={
            "id":sessao.id,
            "id_cronograma":sessao.cronograma.id,
            "id_palestrante":sessao.palestrante.id,
            "titulo":sessao.titulo,
            "descricao":sessao.descricao,
            "NomePalestrante":sessao.palestrante.nome,
            "curriculoPalestrante":sessao.palestrante.curriculo,
            "local":sessao.cronograma.local,
            "DT_Hora_inicio": sessao.cronograma.data_hora_inicio.strftime("%Y-%m-%dT%H:%M"),
            "DT_Hora_fim": sessao.cronograma.data_hora_fim.strftime("%Y-%m-%dT%H:%M")
        }
        sessao_data.append(data)
    return sessao_data
def Dicionario_de_Palestra(evento:Evento):
    cronograma= Cronograma.objects.filter(evento_id= evento.id)
    sessao = Sessao.objects.filter(cronograma__in=cronograma).first()
    data={
        "id":evento.id,
        "id_sessao":sessao.id,
        "id_cronograma":sessao.cronograma.id,
        "id_palestrante":sessao.palestrante.id,
        "titulo":evento.titulo,
        "tema":evento.tema,
        "descricao":evento.descricao,
        "curso":evento.curso,
        "nomePalestrante":sessao.palestrante.nome,
        "breve_curriculo":sessao.palestrante.curriculo,
        "data":evento.dt_inicio.strftime("%Y-%m-%d"),
        "hora_inicio":evento.dt_inicio.timetz(),
        "hora_fim":evento.dt_fim.timetz(),
        "dt_inicio_inscricao":evento.dt_inicio_inscricao.strftime("%Y-%m-%dT%H:%M"),
        "dt_fim_inscricao":evento.dt_fim_inscricao.strftime("%Y-%m-%dT%H:%M"),
        "limite_inscricao":evento.limite_inscricao,
        "local":sessao.cronograma.local
    }
    return data

    
