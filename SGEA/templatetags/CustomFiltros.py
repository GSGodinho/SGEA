from django import template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

register=template.Library()


def Uid(value):
    return urlsafe_base64_encode(force_bytes(value))

register.filter("UID",Uid)



