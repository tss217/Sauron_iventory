from django.db import models
from django.utils import timezone


class Equipamento(models.Model):
    class Status(models.TextChoices):
        DISPONIVEL = "disponivel", "Disponível"
        EM_USO = "em_uso", "Em uso"
        MANUTENCAO = "manutencao", "Manutenção"

    hhid = models.CharField("HHID", max_length=10, unique=True)
    nome = models.CharField("Equipamento", max_length=60)
    status = models.CharField(
        "Status",
        max_length=20,
        choices=Status.choices,
        default=Status.DISPONIVEL,
    )
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        ordering = ["hhid"]
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"

    def __str__(self):
        return f"{self.hhid} - {self.nome}"

    def save(self, *args, **kwargs):
        self.hhid = self.hhid.strip().upper()
        self.nome = self.nome.strip()
        return super().save(*args, **kwargs)


class Usuario(models.Model):
    id_usuario = models.CharField("ID", max_length=20, unique=True)
    username = models.CharField("Username", max_length=40, unique=True)
    turma = models.CharField("Turma", max_length=1)
    diretrix = models.CharField("Diretrix", max_length=40)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        ordering = ["username"]
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.id_usuario} - {self.username}"

    def save(self, *args, **kwargs):
        self.id_usuario = self.id_usuario.strip()
        self.username = self.username.strip().lower()
        self.turma = self.turma.strip().upper()
        self.diretrix = self.diretrix.strip()
        return super().save(*args, **kwargs)


class Controle(models.Model):
    ORDEM = ["entry_op", "in_lauch", "out_lauch", "out_op"]

    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.PROTECT,
        related_name="controles",
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name="controles",
    )
    data = models.DateField("Data", default=timezone.localdate)

    entry_op = models.DateTimeField("ENTRY-OP", null=True, blank=True)
    in_lauch = models.DateTimeField("IN-LAUCH", null=True, blank=True)
    out_lauch = models.DateTimeField("OUT-LAUCH", null=True, blank=True)
    out_op = models.DateTimeField("OUT-OP", null=True, blank=True)

    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        ordering = ["-data", "equipamento__hhid"]
        verbose_name = "Controle"
        verbose_name_plural = "Controles"
        constraints = [
            models.UniqueConstraint(
                fields=["equipamento", "data"],
                name="controle_unico_equip_dia",
            )
        ]

    def __str__(self):
        return f"{self.data} - {self.equipamento.hhid} - {self.usuario.username}"

    @property
    def proxima_etapa(self):
        for etapa in self.ORDEM:
            if getattr(self, etapa) is None:
                return etapa
        return None

    @property
    def concluido(self):
        return self.out_op is not None

    def pode_registrar(self, etapa):
        if etapa not in self.ORDEM:
            return False
        if getattr(self, etapa) is not None:
            return False

        indice = self.ORDEM.index(etapa)
        if indice == 0:
            return True

        anterior = self.ORDEM[indice - 1]
        return getattr(self, anterior) is not None
