from django.contrib import admin
from .models import Profile,Tb_Registros


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

@admin.register(Tb_Registros)
class Tb_OcorrenciasAdmin(admin.ModelAdmin):
    list_display = ['id_ocorrencia','usuario','data_registro', 'relato','Nome_propriedade','prejuizo','hectares',\
                   'rebanho','latitude', 'longitude','observacao']
    search_fields = ('id_ocorrencia', 'relato')
    ordering = ['relato']

