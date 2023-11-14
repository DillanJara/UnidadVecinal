from rest_framework import serializers
from principal.models import Miembro, Certificado, SolicitudCertificado

class CertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = ['cer_id', 'cer_nombre']

class MiembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miembro
        fields = ['mie_rut', 'mie_dv', 'mie_nombre', 'mie_ap_paterno', 'mie_ap_materno']

class SolicitudCertificadoSerializer(serializers.ModelSerializer):
    miembro_mie = MiembroSerializer(read_only=True)
    certificado_cer = CertificadoSerializer(read_only=True)

    class Meta:
        model = SolicitudCertificado
        fields = ['sol_cer_id', 'sol_cer_fecha', 'sol_cer_familiar', 'sol_cer_rut_familiar', 'miembro_mie', 'certificado_cer']