#Scrape.py
from bs4 import BeautifulSoup
import requests, os, time
import pandas as pd

url = "https://quotes.toscrape.com/page/"
pagina = 1

nome_arquivo = input("Digite um nome para o arquivo: ")
if ".csv" not in nome_arquivo:
    nome_arquivo += ".csv"

while True:
  time.sleep(1)  # "respiro" para o servidor
  print(f"Extraindo pagina: {pagina}", end="\r", flush=True)

  url_completa = f"{url}{pagina}"
  resposta = requests.get(url_completa)

  # Verifica se a página carregou
  if resposta.status_code != 200:
    print(f"Erro ao aceder à página {pagina}. A encerrar.")
    break

  resposta.encoding = "utf-8"
  site = BeautifulSoup(resposta.text, "html.parser")

  # Encontra todos os blocos
  blocos_citacoes = site.find_all("div", class_="quote")

  if not blocos_citacoes:
    print("Nenhuma citação encontrada nesta página.")
    break

  autores = []
  textos = []
  tags = []

  # Extrai os dados de dentro de cada bloco individualmente
  for bloco in blocos_citacoes:
    autor = bloco.find("small", class_="author")
    texto = bloco.find("span", class_="text")
    tag_meta = bloco.find("meta", class_="keywords")

    autores.append(autor.text.strip() if autor else "")
    textos.append(texto.text.strip() if texto else "")
    tags.append(tag_meta["content"] if tag_meta else "")

  dados_dc = {
      "Autor": autores,
      "Texto": textos,
      "Tags": tags
   }

  # Criar e tratar DataFrame
  df_novo = pd.DataFrame(dados_dc)

  if os.path.exists(nome_arquivo):
    df_antigo = pd.read_csv(nome_arquivo)
    df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
    df_final = df_final.drop_duplicates()
  else:
    df_final = df_novo

  df_final.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")

  # Verificar se existe o botão "next" para continuar a paginação
  avancar = site.find("li", class_="next")
  if not avancar:
    print("\nChegamos à última página!")
    break
  else:
    pagina += 1
    
print(f"Seu arquivo {nome_arquivo} foi gerado com Sucesso!")
input("\nAperte 'Enter' para sair")