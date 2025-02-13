from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from .models import Participante

def validarCPF(value:str):

    if re.search("1{11}|2{11}|3{11}|4{11}|5{11}|6{11}|7{11}|8{11}|9{11}",value):
        raise ValidationError( 
            _("%(value)s CPF Invalido"),
            params={"value": value},
        )
    
    validante1=int(value[-2])
    nums_validação2=value[0:9]
    soma1=0

    for Ncpf,multi in zip(nums_validação2,range(10,1,-1)):
        soma1+=(int(Ncpf)*multi)

    validacao1=(soma1*10)%11
    if validacao1== 10:
        validacao1=0

    Etapa1_validacao= validacao1==validante1

    validante2=int(value[-1])
    nums_validação2=value[0:10]


    soma2=0
    for Ncpf,multi in zip(nums_validação2,range(11,1,-1)):
        soma2+=(int(Ncpf)*multi)

    validacao2=(soma2*10)%11
    if validacao2== 10:
        validacao2=0



    Etapa2_validacao=validacao2==validante2
    
    if not(Etapa1_validacao and Etapa2_validacao):
        raise ValidationError(
            _("%(value)s CPF Invalido"),
            params={"value": value},
        )
def validarUnicoUsuario(value:str):
    if Participante.objects.filter(username=value).exists():
        raise ValidationError(
            _("%(value)s já existe alguem com esse usuario"),
            params={"value": value},
        )
def validarUnicoEmail(value:str):
    if Participante.objects.filter(email=value).exists():
        raise ValidationError(
            _("%(value)s já existe alguem com esse email"),
            params={"value": value},
        )