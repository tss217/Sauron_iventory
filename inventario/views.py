from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EquipamentoForm, UsuarioForm
from .models import Controle, Equipamento, Usuario


def cadastro(request):
    equipamentos = Equipamento.objects.all()
    usuarios = Usuario.objects.all()

    form = EquipamentoForm()
    form_usuario = UsuarioForm()
    aba_ativa = "equipamento"

    if request.method == "POST":
        tipo = request.POST.get("form_type")

        if tipo == "equipamento":
            form = EquipamentoForm(request.POST)

            if form.is_valid():
                equipamento = form.save()
                messages.success(
                    request,
                    f"Equipamento {equipamento.hhid} cadastrado com sucesso.",
                )
                return redirect("inventario:cadastro")

        elif tipo == "usuario":
            form_usuario = UsuarioForm(request.POST)

            if form_usuario.is_valid():
                usuario = form_usuario.save()
                messages.success(
                    request,
                    f"Usuário {usuario.username} cadastrado com sucesso.",
                )
                return redirect("inventario:cadastro")

            # Se o form de usuário falhou, reabre a aba de usuário.
            aba_ativa = "usuario"

    contexto = {
        "equipamentos": equipamentos,
        "usuarios": usuarios,
        "form": form,
        "form_usuario": form_usuario,
        "aba_ativa": aba_ativa,
    }

    return render(request, "inventario/cadastro.html", contexto)


def controle(request):
    hoje = timezone.localdate()
    controles = (
        Controle.objects.filter(data=hoje)
        .select_related("equipamento", "usuario")
    )
    usuarios = Usuario.objects.all()

    if request.method == "POST":
        hhid = (request.POST.get("hhid") or "").strip()
        id_usuario = request.POST.get("id_usuario")

        equipamento = Equipamento.objects.filter(hhid__iexact=hhid).first()
        usuario = Usuario.objects.filter(pk=id_usuario).first()

        if not equipamento:
            messages.error(
                request,
                f'Equipamento "{hhid}" não encontrado. Cadastre-o primeiro.',
            )
        elif equipamento.status == Equipamento.Status.MANUTENCAO:
            messages.error(request, "Este equipamento está em manutenção.")
        elif equipamento.status == Equipamento.Status.EM_USO and not Controle.objects.filter(
            equipamento=equipamento, data=hoje
        ).exists():
            messages.error(request, "Este equipamento está marcado como em uso.")
        elif not usuario:
            messages.error(request, "Selecione um usuário cadastrado.")
        elif Controle.objects.filter(equipamento=equipamento, data=hoje).exists():
            messages.error(
                request,
                "Este equipamento já está no controle de hoje. Continue pela tabela.",
            )
        else:
            Controle.objects.create(
                equipamento=equipamento,
                usuario=usuario,
                entry_op=timezone.now(),
            )
            equipamento.status = Equipamento.Status.EM_USO
            equipamento.save(update_fields=["status"])
            messages.success(
                request,
                f"Entrada de {equipamento.hhid} registrada para {usuario.username}.",
            )
            return redirect("inventario:controle")

    contexto = {
        "controles": controles,
        "usuarios": usuarios,
        "hoje": hoje,
        "hhid_digitado": request.POST.get("hhid", "") if request.method == "POST" else "",
        "usuario_selecionado": request.POST.get("id_usuario", "") if request.method == "POST" else "",
    }
    return render(request, "inventario/controle.html", contexto)


def buscar_equipamento(request, hhid):
    equipamento = Equipamento.objects.filter(hhid__iexact=hhid.strip()).first()

    if equipamento is None:
        return JsonResponse({"erro": "Equipamento não encontrado."}, status=404)

    return JsonResponse(
        {
            "hhid": equipamento.hhid,
            "nome": equipamento.nome,
            "status": equipamento.status,
            "status_label": equipamento.get_status_display(),
        }
    )


def controle_etapa(request, controle_id):
    if request.method != "POST":
        return redirect("inventario:controle")

    controle = get_object_or_404(
        Controle.objects.select_related("equipamento"),
        pk=controle_id,
    )
    etapa = request.POST.get("etapa")

    if not controle.pode_registrar(etapa):
        messages.error(request, "Etapa inválida ou fora de ordem.")
        return redirect("inventario:controle")

    setattr(controle, etapa, timezone.now())
    controle.save(update_fields=[etapa])

    if etapa == "out_op":
        equipamento = controle.equipamento
        equipamento.status = Equipamento.Status.DISPONIVEL
        equipamento.save(update_fields=["status"])
        messages.success(request, f"Saída de {equipamento.hhid} registrada.")
    else:
        nome_etapa = etapa.replace("_", "-").upper()
        messages.success(
            request,
            f"{nome_etapa} registrado para {controle.equipamento.hhid}.",
        )

    return redirect("inventario:controle")



