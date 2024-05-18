
# Financial Information

### Code Challenge

Código utilizando Python utilizando a API do Google Cloud Platform e Yahoo Finance.

## Instalação

Para rodar o projeto você primeiro deve instalar as bibliotecas presentes dentro do aquivo requirements.txt da seguinte forma

```
    pip install -r requirements.txt
```

Após o download das bibliotecas, é necessário criar uma conta de serviço dentro do Google Cloud Platform para que tenhamos as credencias de acesso da API para manipularmos planilhas.

Crie uma pelo seguinte site
```
    https://console.cloud.google.com/iam-admin/serviceaccounts
```

Assim que criar, gere um arquivo json com as credencias dessa conta de serviço para que possa criar, escrever e salvar planilhas google.

Com o Json dentro do projeto, declare o caminho dele a variável json_path:

```
    json_path = 'caminho_do_seu_json'
```

Após declarar o caminho, basta criar um nome para a planilha na variavel sheet_name e rodar o código:

```
    sheet_name = 'nome_da_sua_planilha'
```

Ao final, irá mostrar o link da planilha no console, onde foi escrito dados sobre as Empresas especificadas dentro da lista symbols.

```
    symbols = ['Petr4.SA', 'VALE3.SA', 'CSNA3.SA']
```