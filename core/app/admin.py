from django.contrib import admin
from .models import Colaborador
from .models import PlanilhaRegistro

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'valor_comissao', 'comissao_paga', 'data_registro')
    search_fields = ('nome', 'email')
    list_filter = ('comissao_paga',)

@admin.register(PlanilhaRegistro)
class PlanilhaRegistroAdmin(admin.ModelAdmin):
    # Quais colunas vão aparecer na lista do painel
    list_display = (
        'cliente', 
        'cpf_cnpj', 
        'tipo_certificado', 
        'valor_venda', 
        'pago_venda', 
        'data_vencimento'
    )
    
    # Cria uma barra de pesquisa buscando por esses campos
    search_fields = ('cliente', 'cpf_cnpj', 'email', 'telefone1')
    
    # Cria um menu lateral de filtros rápidos
    list_filter = ('pago_venda', 'pago_comissao', 'tipo_certificado')
    
    # Ordena os registros dos mais recentes para os mais antigos
    ordering = ('-data_registro',)