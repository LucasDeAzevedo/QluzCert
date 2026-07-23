# QCert Manager

Painel interno (Django + JS puro) para gestão de vendas de certificados digitais (e-CPF/e-CNPJ): clientes, parceiros, tabela de preços, renovações e pagamentos, com um livro de vendas sincronizado via Google Sheets.

## Estrutura do projeto

- `core.app_Gestor` — app ativo, roteado em `core/urls.py`. Toda view, template e arquivo estático novo deve entrar aqui.
- `core.app` — não tem nenhuma URL própria. Existe só para manter os modelos `PlanilhaRegistro`/`Colaborador` e os serviços de importação/exportação do Google Drive (`services.py`) que `app_Gestor` importa. Não adicione views, templates ou estáticos novos aqui.

## Configuração

1. Crie e ative um virtualenv, depois instale as dependências:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Variáveis de ambiente (opcionais, têm valor padrão para desenvolvimento):
   - `MERCADO_PAGO_ACCESS_TOKEN` — token de acesso da API do Mercado Pago, necessário para gerar pagamentos PIX reais.
   - `GOOGLE_SHEET_ID` — ID da planilha do Google Drive usada para sincronizar clientes/parceiros (tem um valor padrão em `core/settings.py`, sobrescreva se for usar outra planilha).
3. Coloque o `credentials.json` (Service Account do Google com acesso à planilha/Drive) na raiz do projeto. Esse arquivo é ignorado pelo git — nunca o adicione ao versionamento.
4. Rode as migrações e inicie o servidor:
   ```
   python manage.py migrate
   python manage.py runserver
   ```

## Limitações conhecidas

- **Nenhum endpoint exige login.** O projeto não usa `django.contrib.auth` em nenhuma view — é adequado apenas para uso interno em rede restrita, não para exposição pública, até que autenticação seja adicionada.
- Não há suíte de testes automatizados; os scripts em `scripts/` são checagens manuais, não testes de CI.
