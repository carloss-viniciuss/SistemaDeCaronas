from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.http import HttpResponse
from .models import Passageiro, RegistroCarona


def registrar_caronas(request):
    hoje = timezone.now().date()

    if request.method == 'POST':
        passageiro_id = request.POST.get('passageiro_id')
        tipo = request.POST.get('tipo')

        if passageiro_id and tipo:
            passageiro = get_object_or_404(Passageiro, id=passageiro_id)
            RegistroCarona.objects.create(
                passageiro=passageiro,
                tipo=tipo,
                data=hoje
            )
            messages.success(request, f"Carona de {passageiro.nome} registrada!")
            return redirect('registrar_caronas')

    passageiros = Passageiro.objects.filter(ativo=True)
    return render(request, 'caronas/registrar.html', {'passageiros': passageiros, 'hoje': hoje})

# 2. CADASTRAR NOVO PASSAGEIRO
def cadastrar_passageiro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        valor = request.POST.get('valor_percurso')

        if nome and valor:
            Passageiro.objects.create(nome=nome, valor_percurso=valor, ativo=True)
            messages.success(request, f"Passageiro {nome} cadastrado com sucesso!")
            return redirect('registrar_caronas')

    return render(request, 'caronas/cadastrar_passageiro.html')

# 3. VISUALIZAR O DIA ATUAL E EDITAR
def visualizar_dia(request):
    hoje = timezone.now().date()
    registros = RegistroCarona.objects.filter(data=hoje).select_related('passageiro')
    total_dia = registros.aggregate(Sum('valor_total'))['valor_total__sum'] or 0.00

    return render(request, 'caronas/visualizar_dia.html', {
        'registros': registros,
        'hoje': hoje,
        'total_dia': total_dia
    })

def editar_carona(request, pk):
    carona = get_object_or_404(RegistroCarona, pk=pk)
    if request.method == 'POST':
        novo_tipo = request.POST.get('tipo')
        if novo_tipo:
            carona.tipo = novo_tipo
            carona.save() # Recalcula valor automaticamente no save()
            messages.success(request, "Registro alterado com sucesso!")
            return redirect('visualizar_dia')

    return render(request, 'caronas/editar_carona.html', {'carona': carona})

def deletar_carona(request, pk):
    carona = get_object_or_404(RegistroCarona, pk=pk)
    if request.method == 'POST':
        carona.delete()
        messages.success(request, "Registro removido com sucesso!")
        return redirect('visualizar_dia')
    return render(request, 'caronas/deletar_confirmar.html', {'carona': carona})

# 4. FECHAR CONTA POR PASSAGEIRO
def fechar_conta(request):
    passageiros = Passageiro.objects.filter(ativo=True)
    dados = []

    for p in passageiros:
        caronas_pendentes = p.caronas.filter(pago=False).order_by('data')
        total_pendente = caronas_pendentes.aggregate(Sum('valor_total'))['valor_total__sum'] or 0.00
        dados.append({
            'passageiro': p,
            'caronas': caronas_pendentes,
            'total': total_pendente,
            'qtd': caronas_pendentes.count()
        })

    return render(request, 'caronas/fechar_conta.html', {'dados': dados})

# 5. GERADOR DE PDF DE COBRANÇA
def gerar_pdf_cobranca(request, passageiro_id):
    passageiro = get_object_or_404(Passageiro, id=passageiro_id)
    caronas_pendentes = passageiro.caronas.filter(pago=False).order_by('data')
    total = caronas_pendentes.aggregate(Sum('valor_total'))['valor_total__sum'] or 0.00

    # Usamos o HTML imprimível do navegador como PDF limpo
    return render(request, 'caronas/pdf_cobranca.html', {
        'passageiro': passageiro,
        'caronas': caronas_pendentes,
        'total': total,
        'data_emissao': timezone.now()
    })