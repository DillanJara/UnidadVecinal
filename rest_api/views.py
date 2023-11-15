from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from principal.models import SolicitudCertificado, Miembro
from .serializers import SolicitudCertificadoSerializer
# Create your views here.
@api_view(['GET'])
def validarCertificado(request, sol_cer_id, mie_rut):
    try:
        miembro = Miembro.objects.get(mie_rut=mie_rut)
        solicitudCertificado = SolicitudCertificado.objects.get(sol_cer_id=sol_cer_id, miembro_mie=miembro)
        serializer = SolicitudCertificadoSerializer(solicitudCertificado)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
