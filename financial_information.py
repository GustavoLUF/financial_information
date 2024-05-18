"""
Desenvolva um módulo python que baixe informações financeiras de empresas da bolsa de valores 
(Petrobras, Vale, CSN, etc), tais como: balanços, resultados, indicadores,  etc.
"""

import yfinance as yf
import pandas as pd
import gspread
from google.auth import exceptions
from google.oauth2 import service_account
from datetime import datetime, timedelta

symbols = ['Petr4.SA', 'VALE3.SA', 'CSNA3.SA']

sheet_name = 'Financial_Information'

json_path = 'yahoo-finance-413015-091a4ac5cb37.json'

def authenticate_google_sheet(json_path):
    try:
        credential = service_account.Credentials.from_service_account_file(
            json_path, scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        )
        gcredential = gspread.authorize(credential)
        return gcredential
    except exceptions.GoogleAuthError as e:
        print(f"Erro na autenticação: {e}")
        return None

def get_historical_data(symbols):
    final_date = datetime.today().strftime('%Y-%m-%d')
    initial_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    data =  yf.download(symbols, start=initial_date, end=final_date).reset_index()
    return data

def get_financial_data(ticker):
    company = yf.Ticker(ticker)
    balance_sheet = company.balance_sheet
    income_statment = company.financials
    cash_flow = company.cashflow
    return balance_sheet, income_statment, cash_flow

def convert_timestamps(data):
    for col in data.columns:
        if data[col].dtype == 'datetime64[ns]':
            data[col] = data[col].astype(str)
        elif isinstance(data.index, pd.DatetimeIndex):
            data.index = data.index.astype(str)
    return data


def write_google_sheet(sheet, data, worksheet_title):
    try:
        worksheet = sheet.worksheet(worksheet_title)
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=worksheet_title, rows="300", cols="20")
    
    data = convert_timestamps(data)
    data = data.applymap(lambda x: str(x) if isinstance(x, float) else x)
    data_values = data.values.tolist()
    worksheet.update([data.columns.values.tolist()] + data_values)

def make_sheet_public(sheet):
    try:
        sheet.share('', perm_type='anyone', role='reader')
        print("Planilha tornada pública com sucesso!")
    except Exception as e:
        print(f"Erro ao tornar a planilha pública: {e}")

gcredential = authenticate_google_sheet(json_path)

if gcredential:
    
    try:
        sheet = gcredential.open(sheet_name)
        print(f"Planilha '{sheet_name}' encontrada. Escrevendo dados...")
    except gspread.SpreadsheetNotFound:
        print(f"A planilha '{sheet_name}' não existe. Criando uma nova...")
        sheet = gcredential.create(sheet_name)
        sheet_id = sheet.id
        sheet = gcredential.open_by_key(sheet_id)
        # print(f"Link para a nova planilha: {sheet.url}")
        make_sheet_public(sheet)


    for symbol in symbols:
        print(f"Escrevendo dados históricos para o símbolo {symbol}")
        historical_data = get_historical_data(symbol)
        write_google_sheet(sheet, historical_data, symbol + '_Histórico')

        print(f"Escrevendo dados financeiros para o símbolo {symbol}")
        balance_sheet, income_statement, cash_flow = get_financial_data(symbol)

        write_google_sheet(sheet, balance_sheet, symbol + '_Balanço')
        write_google_sheet(sheet, income_statement, symbol + '_Resultados')
        write_google_sheet(sheet, cash_flow, symbol + '_FluxoCaixa')

print(f"""
    ===============================================================
    Link para a planilha: {sheet.url}
    ===============================================================
        """)