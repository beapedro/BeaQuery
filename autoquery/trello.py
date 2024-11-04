import requests
import json

token =  #token trello
key = #chave api trello
trello_list = #id da lista trello


def anexar_arquivo(id,file):
 url = f"https://api.trello.com/1/cards/{id}/attachments"
 
 

 headers = {
        "Accept": "application/json",
 
    }
 query = {
 'key': key,
 'token': token,
 
  }
  
 with open(file, 'rb') as file:
        files = {
            'file': file
        }
        
        response = requests.post(
            url,
            headers=headers,
            params=query,
            files=files
        )
    
  
 
 if response.status_code == 200:
        try:
            data = response.json()
            print("Arquivo anexado com sucesso:")
            print(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e} - Resposta recebida: {response.text}")
 else:
        print(f"Erro ao anexar arquivo ao card: {response.status_code} - {response.text}")


def criartarefa(titulo, descricao, file):
    url = "https://api.trello.com/1/cards"


    headers = {
        "Accept": "application/json"
    }

    query = {
        'idList': trello_list,
        'key': key,
        'token': token,
        'name': titulo,
        'desc': descricao,
        'idLabels': ['67211f9aa8d06bbfc1be4116'],

    }   
    
  
    response = requests.post(url, headers=headers, json=query)

    if response.status_code == 200 or response.status_code == 201:
        try:
            data = response.json()
            card_id = data['id']
            print(f"Cartão criado com sucesso! ID: {card_id}")
            print(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))
            atualizar_cover(card_id)
            anexar_arquivo(card_id,file)   
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e} - Resposta recebida: {response.text}")
    else:
        print(f"Erro na criação do cartão: {response.status_code} - {response.text}")

def atualizar_cover(card_id):
    trello_api = "https://api.trello.com"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

 
    cover_data = {
        "cover": {
            "color": "red",   
            "idAttachment": None,
            "idUploadedBackground": None,
            "size": "normal",
            "brightness": "light"
        },
        'key':  key,
        'token':  token
    }

 
    response = requests.put(f"{trello_api}/1/cards/{card_id}", headers=headers, json=cover_data)

    if response.status_code == 200:
        try:
            data = response.json()
            print("Capa atualizada com sucesso:")
            print(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e} - Resposta recebida: {response.text}")
    else:
        print(f"Erro ao atualizar a capa: {response.status_code} - {response.text}")
        
        
        
def cards_list():
    url = 'https://api.trello.com/1/lists/67211f376a9a55a0301ba798/cards'

    headers = {
        "Accept": "application/json"
    }

    query = {
        'key': key,
        'token': token
    }

   
    response = requests.get(url, headers=headers, params=query)

   
    if response.status_code == 200:
        try:
            data = json.loads(response.text)
            print(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e} - Resposta recebida: {response.text}")
    else:
        print(f"Erro na solicitação: {response.status_code} - {response.text}")
        
            
    return data

def delete_card(id):
 
 
    url = f"https://api.trello.com/1/cards/{id}"

    query = {
    'key': key,
    'token': token
    }

    response = requests.request(
    "DELETE",
    url,
    params=query
    )

    print(response.text)