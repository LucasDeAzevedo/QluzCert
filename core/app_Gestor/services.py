import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pandas as pd


def save_state_to_drive(state, file_id):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    creds_path = os.path.join(project_root, 'credentials.json')
    if not os.path.exists(creds_path):
        raise FileNotFoundError('credentials.json não encontrado para autenticação Google.')

    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)

    clientes = state.get('clientes', []) or []
    parceiros = state.get('parceiros', []) or []
    precos = state.get('precos', []) or []

    df_clientes = pd.DataFrame(clientes)
    df_parceiros = pd.DataFrame(parceiros)
    df_precos = pd.DataFrame(precos)

    pasta_offline = os.path.join(project_root, 'copias_offline')
    if not os.path.exists(pasta_offline):
        os.makedirs(pasta_offline)

    caminho_arquivo_local = os.path.join(pasta_offline, 'estado_clientes_parceiros.xlsx')
    with pd.ExcelWriter(caminho_arquivo_local, engine='openpyxl') as writer:
        if not df_clientes.empty:
            df_clientes.to_excel(writer, sheet_name='Clientes', index=False)
        else:
            pd.DataFrame([{'info': 'Nenhum cliente'}]).to_excel(writer, sheet_name='Clientes', index=False)
        if not df_parceiros.empty:
            df_parceiros.to_excel(writer, sheet_name='Parceiros', index=False)
        else:
            pd.DataFrame([{'info': 'Nenhum parceiro'}]).to_excel(writer, sheet_name='Parceiros', index=False)
        if not df_precos.empty:
            df_precos.to_excel(writer, sheet_name='Precos', index=False)
        else:
            pd.DataFrame([{'info': 'Nenhum preco'}]).to_excel(writer, sheet_name='Precos', index=False)

    media = MediaFileUpload(
        caminho_arquivo_local,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        resumable=True
    )
    drive_service.files().update(fileId=file_id, media_body=media).execute()
    return True
