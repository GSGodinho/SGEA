from django.db import models
from django.contrib.auth.models import AbstractUser

class Evento(models.Model):
    titulo = models.CharField(max_length=255)
    dt_inicio = models.DateTimeField()
    dt_fim = models.DateTimeField()
    tema = models.CharField(max_length=255)
    descricao= models.TextField(max_length=1024)
    dt_inicio_inscricao = models.DateTimeField()
    dt_fim_inscricao = models.DateTimeField()
    perc_necess_cert = models.IntegerField(default=100)
    cert_por_palestra = models.BooleanField(default=False)

    curso_choice={
        "TI":"Tecnico de Informatica",
        "PDG": "Pedagogia",
    }
    tipo_choice={
        "Workshop":"Workshop",
        "Evento" : "Evento",
        "Palestra": "Palestra",
    }
    tipo=models.CharField(max_length=255,choices=tipo_choice)
    limite_inscricao=models.IntegerField(null=True)
    curso=models.CharField(max_length=255,choices=curso_choice)
    
    def __str__(self):
        return self.titulo

class Cronograma(models.Model):
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    local = models.CharField(max_length=255,null=True)
    assunto = models.CharField(max_length=255,null=True)
    evento= models.ForeignKey(Evento,related_name='cronogramas',on_delete=models.CASCADE,)

    def __str__(self):
        return f"{self.assunto}+{self.data_hora_inicio} to {self.data_hora_fim}"
    
class Palestrante(models.Model):
    nome = models.CharField(max_length=255,blank=True)
    curriculo = models.TextField(blank=True)
    foto = models.ImageField(upload_to='palestrantes/fotos/',null=True,blank=True)

    def __str__(self):
        return self.nome

class Sessao(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(null=True)
    cronograma = models.ForeignKey(Cronograma,related_name='sessoes' ,on_delete=models.CASCADE)
    palestrante = models.ForeignKey(Palestrante, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Participante(AbstractUser):
    Nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)
    Nome_social= models.CharField(max_length=255,null=True,blank=True)
    email= models.EmailField(max_length=255)

class Participante_Externo(models.Model):
    participante = models.OneToOneField(Participante, on_delete=models.CASCADE, primary_key=True,related_name='participanteEX')
    telefone = models.CharField(max_length=11,null=True)
    endereco = models.CharField(max_length=255,null=True)
    instituicao = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.participante.nome

class Participante_Interno(models.Model):
    participante = models.OneToOneField(Participante, on_delete=models.CASCADE, primary_key=True)
    matricula = models.CharField(max_length=20)
    ativo = models.BooleanField()

    def __str__(self):
        return self.participante.nome

class Sessao_Participante(models.Model):
    confirmacao = models.BooleanField(default=False)
    Sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('Sessao', 'participante'),)

    def __str__(self):
        return f"{self.participante.Nome} - {self.Sessao.titulo}"
