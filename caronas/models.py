from django.db import models
from django.utils import timezone

class Passageiro(models.Model):
    nome = models.CharField(max_length=100)
    valor_percurso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Valor cobrado por trecho único",
    )
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class RegistroCarona(models.Model):
    TIPO = [('IDA', 'Apenas ida'),
            ('VOLTA', 'Apenas volta'),
            ('IDA_VOLTA', 'Ida e Volta'),
        ]

    passageiro = models.ForeignKey(Passageiro, on_delete=models.CASCADE, related_name='caronas')
    data = models.DateField(default=timezone.now)
    tipo = models.CharField(max_length=15, choices=TIPO)
    valor_total = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    pago = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.tipo == 'IDA_VOLTA':
            self.valor_total = self.passageiro.valor_percurso*2
        else: 
            self.valor_total = self.passageiro.valor_percurso

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.passageiro.nome} - {self.data} ({self.get_tipo_display()})"

    

