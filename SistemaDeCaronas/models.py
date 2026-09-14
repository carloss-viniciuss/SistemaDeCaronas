from django.db import models

class Passageiro(models.Model):
    nome = models.CharField(max_length=100)
    quant_trajetos = models.PositiveIntegerField(default=0)
    valor_atual = models.DecimalField(max_digits=5, decimal_places=2)

