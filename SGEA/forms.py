from django import forms
from .models import Evento,Participante,Participante_Externo,Cronograma,Sessao
from django.core import validators
from .CustomValidators import validarCPF,validarUnicoUsuario,validarUnicoEmail
from django.contrib.auth.forms import SetPasswordMixin
from django.contrib.auth.password_validation import validate_password

#Form referente a Evento do tipo Evento
class EventoForm(forms.Form):
    id=forms.IntegerField(
        label="",
        required=False,
        widget=forms.HiddenInput()
    )
    titulo = forms.CharField(
        max_length=255,
        label= "titulo do Evento",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control'})
        )
    tema = forms.CharField(
        max_length=255,
        label="tema",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control'})
        )
    
    curso = forms.ChoiceField(
        label="Curso",
        required=True,
        widget=forms.Select(attrs={'class':'form-control'}),
        choices=Evento.curso_choice
        )
        
    dt_inicio = forms.DateTimeField(
        label="Data de inicio",
        required=True,
        widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'})
        )
    dt_fim = forms.DateTimeField(
        label="Data de Fim",
        required=True,
        widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'})
        )

    dt_inicio_inscricao = forms.DateTimeField(
        label="Inicio da Inscrição",
        required=True,
        widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'})
        )
    dt_fim_inscricao = forms.DateTimeField(
        label="Fim da Inscrição",
        required=True,
        widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'})
        )
    
    perc_necess_cert = forms.IntegerField(
        max_value=100,
        required=True,
        label="Porcentagem Necessaria para Certificado",
        widget=forms.NumberInput(attrs={'class':'form-control'})
        )
    
    cert_por_palestra = forms.BooleanField(
        label="Certificado por Palestra?",
        required=True,
        widget=forms.CheckboxInput(attrs={'class':'form-control'})
        )
    
    limite_inscricao = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={'class':'form-control'})
    )
    descricao= forms.CharField(
        required=True,
        max_length=1000,
        widget=forms.Textarea(attrs={'class':'form-control'})
    )

    def clean(self):
        cleaned_data=super().clean()
        dt_inicio_inscricao=cleaned_data.get("dt_inicio_inscricao")
        dt_fim_inscricao=cleaned_data.get("dt_fim_inscricao")
        dt_inicio=cleaned_data.get("dt_inicio")
        dt_fim=cleaned_data.get("dt_fim")

        if dt_inicio_inscricao>dt_fim_inscricao:
            self.add_error("dt_fim_inscricao","O Temino da Inscricao não pode acontecer antes do inicio da inscrição")
        elif dt_inicio>dt_fim:
            self.add_error("dt_fim","O Temino do Evento não pode acontecer antes do inicio")
        elif dt_fim_inscricao>dt_inicio:
            self.add_error("dt_inicio","O inicio do Evento tem que ser após o fim da Inscricao")
        elif dt_fim==dt_inicio:
            self.add_error("dt_inicio","o inicio do Evento e o Termino do Evento não pode ser identicos")
        elif dt_fim_inscricao==dt_inicio_inscricao:
            self.add_error("dt_inicio_inscricao","o inicio da inscriçao e o Termino da inscriçao não pode ser identicos")
        
        return cleaned_data
    
    def initialUpdate(self,evento):
        self.initial={
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
    def save(self,**kwargs):
        EventoInsert=super().clean()
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
                "tipo" :"Evento",
                "limite_inscricao" :EventoInsert['limite_inscricao'],
                "curso" :EventoInsert['curso']
            }       
        )
        return EventoNovo
#Form referente ao cadastro de Palestras no cadastro de Eventos
class SessaoForm(forms.Form):
    id=forms.IntegerField(
        required=False,
        label="",
        widget=forms.HiddenInput() 
    )
    id_cronograma=forms.IntegerField(
        required=False,
        label="",
        widget=forms.HiddenInput() 
    )
    id_palestrante=forms.IntegerField(
        required=False,
        label="",
        widget=forms.HiddenInput() 
    )
    
    titulo=forms.CharField(
        label="Título da Sessão",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    descricao= forms.CharField(
        max_length=1000,
        label="Descricao da Sessão",
        widget= forms.Textarea(attrs={'class':'form-control'})
    )

    NomePalestrante = forms.CharField(
        max_length=255,
        label="Nome do Palestrante",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control'})
        )
    curriculoPalestrante= forms.CharField(
        max_length=1000,
        label="Breve Curriculo do Palestrante",
        widget= forms.Textarea(attrs={'class':'form-control'})
    )
    local=forms.CharField(
        max_length=255,
        label="Local",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    DT_Hora_inicio=forms.DateTimeField(
        label="Horario de inicio",
        required=True,
        widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'})
    )
    DT_Hora_fim=forms.DateTimeField(
        label="Horario de Fim",
        required=True,
        widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'})
    )
    def clean(self):
        cleaned_data=super().clean()
        DT_Hora_fim=cleaned_data.get("DT_Hora_fim")
        DT_Hora_inicio=cleaned_data.get("DT_Hora_inicio")
        if DT_Hora_fim<DT_Hora_inicio:
            self.add_error("DT_Hora_fim","A Hora de Fim tem que ser depois do inicio")
        if DT_Hora_fim==DT_Hora_inicio:
            self.add_error("DT_Hora_inicio","A Hora de Fim Não pode Ser Identica a Hora de Inicio")
        return cleaned_data

#Form referenciado no processo de inscrição de Cronogramas no cadastro do Evento e Palestras
class CronogramaForm(forms.Form):
    id=forms.IntegerField(
        required=False,
        label="",
        widget=forms.HiddenInput()
    )
    Assunto=forms.CharField(
        max_length=255,
        label="Assunto",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    local=forms.CharField(
        max_length=255,
        label="Local",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    DT_Hora_inicio=forms.DateTimeField(
        label="Horario de inicio",
        required=True,
        widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'})
    )
    DT_Hora_fim=forms.DateTimeField(
        label="Horario de Fim",
        required=True,
        widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'})
    )

    def clean(self):
        cleaned_data=super().clean()
        DT_Hora_fim=cleaned_data.get("DT_Hora_fim")
        DT_Hora_inicio=cleaned_data.get("DT_Hora_inicio")
        if DT_Hora_fim<DT_Hora_inicio:
            self.add_error("DT_Hora_fim","A Hora de Fim tem que ser depois do inicio")
        if DT_Hora_fim==DT_Hora_inicio:
            self.add_error("DT_Hora_inicio","A Hora de Fim Não pode Ser Identica a Hora de Inicio")
        return cleaned_data

#Form Responsavel por Participante ,só é valido para participante externo,o sistema não é capaz de registar internos
"""class ParticipanteForm(form.forms):
    nome = forms.CharField(
        max_length=255,
        label="Nome",
        widget=forms.TextInput(attrs={'class':'form-control'}),
    )
    #Se utilizar no Lugar do Nome para casos exista
    nomeSocial = forms.CharField(
        max_length=255,
        label="Nome Social",
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=False
    )

    usuario = forms.CharField(
        max_length=127,
        label="Usuario",
        widget=forms.TextInput(attrs={'class':'form-control'}),
        )
    
    senha = forms.CharField(
        min_length=8,
        max_length=127,
        label="senha",
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        )
    
    confirmarSenha = forms.CharField(
        min_length=8,
        max_length=127,
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        )
    
    email = forms.EmailField(
        max_length=255,
        label="Email",
        widget=forms.EmailInput(attrs={'class':'form-control'}),
        validators=[validators.EmailValidator],
        )
    
    telefone= forms.CharField(
        max_length=11,
        label="Telefone",
        widget=forms.TextInput(attrs={'class':'form-control'}),
        validators=[validators.RegexValidator(regex="D",message="Insira Apenas Números",inverse_match=True)],
        )
    
    cpf = forms.CharField(
        min_length=11,
        max_length=11,
        label="CPF",
        widget=forms.TextInput(attrs={'class':'form-control'}),
        validators=[validateCPF],
        )
    
    def clean(self):
        cleaned_data=super().clean()
        senha=  cleaned_data.get("senha")
        confirmarSenha=cleaned_data.get("confirmarSenha")
        #valida se as daus senhas são iguais se não forem manda adiciona Erros
        if senha!=confirmarSenha:
            self.add_error("senha","As Senhas devem coincidir")
            self.add_error("confirmarSenha","As Senhas devem coincidir")
        else:
            return cleaned_data
            """
#Form referente ao cadastro do Evento Tipo Palestra
class PalestraForm(forms.Form):
    id=forms.IntegerField(
        required=False,
        label="",
        widget=forms.HiddenInput()
    )

    id_cronograma=forms.IntegerField(
        required=False,
        label="",
        widget=forms.HiddenInput()
    )

    id_palestrante=forms.IntegerField(
        required=False,
        label="",
        widget=forms.HiddenInput()
    )
    id_sessao=forms.IntegerField(
        required=False,
        label="",
                widget=forms.HiddenInput()

    )

    titulo = forms.CharField(
        max_length=255,
        label= "Titulo da Palestra",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo'})
        )
    tema = forms.CharField(
        max_length=255,
        label="tema",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Tema'})
        )
    descricao= forms.CharField(
        max_length=1000,
        label="Descricao da Palestra",
        widget= forms.Textarea(attrs={'class':'form-control','placeholder':'Descrição da Palestra'})
    )
    curso = forms.ChoiceField(
        label="Curso",
        widget=forms.Select(attrs={'class':'form-control'}),
        required=True,
        choices=Evento.curso_choice
    )
    
    nomePalestrante = forms.CharField(
        max_length=255,
        label= "Nome Palestrante",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nome do Palestrante'})
        )
    
    breve_curriculo= forms.CharField(
        max_length=1000,
        label="Breve Curriculo do Palestrante",
        widget=forms.Textarea(attrs={'class':'form-control','placeholder':'breve curriculo do Palestrane'})
    )
    local=forms.CharField(
        max_length=255,
        label="Local",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Local'})
        )
    
    data=forms.DateField(
        label="Data",
        required=True,
        widget=forms.DateInput(attrs={'class':'form-control','type':'date'})
    )
    
    hora_inicio = forms.TimeField(
        label="Horario de inicio",
        required=True,
        widget=forms.TimeInput(attrs={'class':'form-control','type':'time'})
        )
    hora_fim = forms.TimeField(
        label="Horario de Fim",
        required=True,
        widget=forms.TimeInput(attrs={'class':'form-control','type':'time'})
        )
    
    dt_inicio_inscricao = forms.DateTimeField(
        label="Inicio da Inscrição",
        widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'})
        )
    dt_fim_inscricao = forms.DateTimeField(
        label="Fim da Inscrição",
        widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'})
        )
    
    limite_inscricao = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Numero Maximo de Inscritos'})
    )
    def initialUpdate(self,evento):
        cronograma= Cronograma.objects.filter(evento_id= evento.id)
        sessao = Sessao.objects.filter(cronograma__in=cronograma).first()
        self.initial={
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
 
class AlunoForm(forms.Form):
    nome = forms.CharField(
        max_length=255,
        label="Nome",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        validators=[validarUnicoEmail]
    )
    telefone= forms.CharField(
        max_length=11,
        label="Telefone",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Telefone com DDD'}),
        validators=[validators.RegexValidator(regex="D",message="Insira Apenas Números",inverse_match=True)],
    )
    cpf = forms.CharField(
        max_length=11,
        label="CPF",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'}),
        validators=[validarCPF]
    )
    matricula = forms.CharField(
        max_length=50,
        label="Matrícula",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'})
    )
    turma = forms.CharField(
        max_length=50,
        label="Turma",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Turma'})
    )
    curso = forms.CharField(
        max_length=100,
        label="Curso",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Curso'})
    )
    usuario = forms.CharField(
        max_length=127,
        label="Usuario",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Usuario'}),
        validators=[validarUnicoUsuario]
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
    )
    confirmarSenha = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Senha'})
    )
    def clean(self):
        cleaned_data=super().clean()
        senha=  cleaned_data.get("senha")
        confirmarSenha=cleaned_data.get("confirmarSenha")
        #valida se as daus senhas são iguais se não forem manda adiciona Erros
        if senha!=confirmarSenha:
            self.add_error("senha","As Senhas devem coincidir")
            self.add_error("confirmarSenha","As Senhas devem coincidir")
        else:
            return cleaned_data

class VisitanteForm(forms.Form,SetPasswordMixin):
    nome = forms.CharField(
        max_length=255,
        label="Nome",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        validators=[validarUnicoEmail]
    )
    telefone= forms.CharField(
        max_length=11,
        label="Telefone",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Telefone com DDD'}),
        validators=[validators.RegexValidator(regex="D",message="Insira Apenas Números",inverse_match=True)],
    )
    cpf = forms.CharField(
        max_length=11,
        label="CPF",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'}),
        validators=[validarCPF]
    )
    instituicao_ensino = forms.CharField(
        max_length=100,
        label="Instituição de Ensino",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instituição de Ensino'})
    )
    usuario = forms.CharField(
        max_length=127,
        label="Usuario",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Usuario'}),
        validators=[validarUnicoUsuario]
        )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Senha',
            'type':'password'}),
        validators=[validate_password]
    )
    confirmarSenha = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirmar Senha',
            'type':'password'})
    )



    def clean(self):
        cleaned_data=super().clean()
        self.validate_passwords(password1_field_name="senha",password2_field_name="confirmarSenha")
        return cleaned_data

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Usuário',
        'class': 'input-field'
    }))
    senha = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha',
        'class': 'input-field',
        'type':'password'
    }))

class userForm(forms.ModelForm):
    
    class Meta:
        model = Participante
        fields = ["Nome","Nome_social","email"]
        widgets = {'Nome':forms.TextInput(attrs={'class':'form-control'}),
                   'Nome_social':forms.TextInput(attrs={'class':'form-control'}),
                   'email':forms.TextInput(attrs={'class':'form-control'})}
    
class userExternoForm(forms.ModelForm):

    class Meta:
        model = Participante_Externo
        fields = ["telefone","instituicao"]
        widgets= {'telefone': forms.TextInput(attrs={'class':'form-control'}),
                  'instituicao': forms.TextInput(attrs={'class':'form-control'})}

