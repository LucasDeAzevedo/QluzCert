#!/usr/bin/env python
import os
import sys
import django
import json
import re

# Adicionar o diretório do projeto ao path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)
os.chdir(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

sys.stdout.reconfigure(encoding='utf-8')

from django.test import Client
from django.test.utils import override_settings

override_settings(ALLOWED_HOSTS=['testserver']).enable()

client = Client()
response = client.get('/')
print(f'Status: {response.status_code}')

if response.status_code == 200:
    content = response.content.decode()
    match = re.search(r'window\.INITIAL_PARCEIROS\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if match:
        parceiros = json.loads(match.group(1))
        print('✓ Aba de Parceiros carregada com sucesso')
        print(f'\nParceiros encontrados: {len(parceiros)}')
        for p in sorted({p.get('nome', '') for p in parceiros}):
            print(f'  - {p}')
    else:
        print('✗ INITIAL_PARCEIROS não encontrado na página do dashboard')
        print(content[:500])
else:
    print(f'✗ Erro HTTP {response.status_code}')
