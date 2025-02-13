from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Palestrante,Sessao,Participante,Cronograma,Evento,Sessao_Participante,Participante_Externo,Participante_Interno

admin.site.register(Palestrante)
admin.site.register(Sessao)
admin.site.register(Sessao_Participante)
admin.site.register(Participante_Interno)
admin.site.register(Participante_Externo)


admin.site.register(Cronograma)
admin.site.register(Evento)
admin.site.register(Participante, UserAdmin)

# Register your models here.
