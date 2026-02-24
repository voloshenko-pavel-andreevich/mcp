from fastmcp import FastMCP
import requests
import io
import pandas as pd
import datetime as date

def get_table_str_11(FILE_ID: str) -> str:

    url = f"https://docs.google.com/spreadsheets/d/{FILE_ID}"

    response = requests.get(url)
    response.encoding = 'utf-8'

    # io.StringIO чтоб показать что это не путь к файлу
    html_data = io.StringIO(response.text)

    try:
        tables = pd.read_html(html_data, header=None)
        if not tables:
            return ""

        df = tables[0]

        df = (df.replace(r'^\s*$', pd.NA, regex=True)
              .dropna(how='all')
              .dropna(axis=1, how='all')
              .fillna('')
              .drop_duplicates())

        return df.astype(str).agg(';'.join, axis=1).str.cat(sep='\n')
    except Exception as e:
        return f"Ошибка парсинга: {e}"

def get_table_list_0(table_str: str) -> list[list[str]]:
    rows = table_str.split('\n')
    matrix = []
    for row in rows:
        matrix.append(row.split(';'))
    return matrix

mcp = FastMCP(
    name="Assistant",
    instructions="Ассистент по анализу таблиц"
)

@mcp.tool
def tables_info(FILE_ID: str) -> list[list[str]]:
    ''' Принимает id файла
        Возвращает таблицу
        Использовать только по запросу
        Исполнителем могут являться организации и люди
        Вызывать не больше одного раза для уникального id файла'''
    table_str = get_table_str_11(FILE_ID)
    table_list = get_table_list_0(table_str)
    return table_list

@mcp.tool
def get_date():
    ''' Возвращает сегодняшнее число'''
    today = date.today()
    return today

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
    #mcp.run(transport='stdio')

