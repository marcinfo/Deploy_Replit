from django.db import models
from django.conf import settings
from stdimage import StdImageField


CULTURAS_CHOICE =(
    ("Milho",'MILHO'),
    ("Arroz","ARROZ"),
    ("Soja","SOJA"),
)
PRAGAS_CHOICE=(
    ("Formiga-rapa-rapa",'Formiga-rapa-rapa'),
    ("Mancha-circular","Mancha-circular"),
    ("Larva-arame","Larva-arame"),
)

class Base(models.Model):
    #inserido = models.DateField('Criado em',auto_now_add=True)
    #atualizado = models.DateField('Modificado em',auto_now_add=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'




class Tb_Registros(Base):
    id_ocorrencia = models.AutoField(primary_key=True)
    usuario =  models.CharField(name='Usuário',max_length=45,null=True,blank=True)
    data_registro =  models.DateField(name='Data da Ocorrência',null=True,blank=True)
    relato = models.CharField(name='Tipo de Praga',max_length=40,null=True,blank=True,choices=PRAGAS_CHOICE)
    cultura =  models.CharField(name='Cultura',max_length=45,null=True,blank=True,choices=CULTURAS_CHOICE)
    Nome_propriedade = models.CharField(name='Nome da Propriedade afetada',max_length=60,null=True,blank=True)
    prejuizo=models.DecimalField(name='Total do prejuizo R$',max_digits=20, decimal_places=2,null=True,blank=True)
    hectares=models.CharField(name='Quantidade de hectar afetado',max_length=4,null=True,blank=True)
    latitude = models.CharField(max_length=45,null=True,blank=True)
    longitude = models.CharField(max_length=45,null=True,blank=True)
    imagem = StdImageField('Imagem',upload_to='images',null=True,blank=True)
    observacao = models.TextField(name='Observações',null=True,blank=True)

    class Meta:

        verbose_name = "Tabela de Registro"
        verbose_name_plural = "Tabela de Registros"
    def __str__(self):
        return self.Usuário



class TbPragas(models.Model):
    id_praga = models.AutoField(primary_key=True)
    cultura = models.CharField(max_length=45, blank=True, null=True)
    especie = models.CharField(max_length=45, blank=True, null=True)
    nome_comum = models.CharField(max_length=45)
    nome_comum2 = models.CharField(max_length=45)

    class Meta:

        verbose_name = "TbPraga"
        verbose_name_plural = "TbPragas"