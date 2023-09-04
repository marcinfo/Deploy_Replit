from django.db import models
from django.conf import settings
import requests
from django.contrib.auth import authenticate, login
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'




class Tb_Registros(models.Model):
    id_ocorrencia = models.AutoField(primary_key=True)
    usuario =  models.CharField(max_length=45,null=True)
    data_registro =  models.CharField(max_length=45,null=True)
    relato = models.CharField(max_length=45)
    Nome_propriedade = models.CharField(max_length=60,blank=True)
    prejuizo=models.FloatField(max_length=60,null=True)
    hectares=models.CharField(max_length=4,null=True)
    rebanho= models.IntegerField(blank=True,null=True)
    latitude = models.CharField(max_length=45)
    longitude = models.CharField(max_length=45)
    observacao = models.TextField()
    class Meta:

        verbose_name = "Tabela de Registro"
        verbose_name_plural = "Tabela de Registros"

class Tb_Pragas(models.Model):
    id_praga = models.AutoField(primary_key=True)
    cultura =  models.CharField(max_length=45,null=True)
    espécie_valida =  models.CharField(max_length=45,null=True)
    nome_comum = models.CharField(max_length=45)
    nome_comum2 = models.CharField(max_length=45)

    class Meta:

        verbose_name = "Tabela de Praga"
        verbose_name_plural = "Tabela de Pragas"