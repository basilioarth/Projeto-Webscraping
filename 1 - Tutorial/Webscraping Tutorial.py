#!/usr/bin/env python
# coding: utf-8

# # Request

# Requests é uma biblioteca fazer requisições HTTP, no caso get, nas páginas que queremos extrair dados.

# In[1]:


# Importando a Requests
import requests

def request_pag(link):
  # Vamos testar a biblioteca requests
  html = requests.get(link)

  # Diferente da urllib, usamos text para apresentar o conteudo que o get nos trouxe
  return html.text

request_pag("https://www.tudogostoso.com.br/")


# # BeautifulSoup

# Com a BeautifulSoup tudo será mais fácil, esta biblioteca do Python serve para extrairmos dados de HTML e XML, de forma 
# fácil e descomplicada podemos acessar os 'nós' da estrutura do HTML da página ou até mesmo classes e pegar as informações.

# In[2]:


# Importando a BeautifulSoup
from bs4 import BeautifulSoup

# URL
url = "https://www.tudogostoso.com.br/"

# lendo a URL 
html = requests.get(url)

# Enfim mostrando o poder da bs4
bs = BeautifulSoup(html.text, 'lxml')

# Imprimindo o título da página
print(bs.title)


# In[3]:


# find_all: todos os elementos encontrados
print(bs.find_all('p'),'\n')


# In[4]:


# find: apenas o primeiro resultado ser extraído
print(bs.find('p'))


# # Categorias de Receitas

# In[5]:


# Encontrando todas as categorias (todas as tags de classe "category-item"):
categorias = bs.find_all('a',class_='category-item')

# Para todas as categorias:
for i in categorias:
#  if i.text in categorias_pra_pular:
#    continue
  # Printamos o texto "em url" que especifica a categoria em questão.
  print(i.text,"->",i['href'],'\n')


# # Receitas por Categoria

# In[6]:


# Encontrando todas as categorias (todas as tags de classe "category-item"):
categorias = bs.find_all('a',class_='category-item')
# url raiz:
url = "https://www.tudogostoso.com.br/"

# Para cada uma das categorias existentes:
for i in categorias:
  print(i.text,':',)
  # Estamos fazendo a requisição da página que contém todas as receitas daquela categoria. 'href' é o texto "em url" que
  # especifica a categoria em questão.
  categoria = request_pag(url+i['href'])
  # Estamos instanciando um objeto BeautifulSoup com a página retornada pela requisição para que possemos extrair os dados
  # desejados.
  categoria_html = BeautifulSoup(categoria, 'lxml')

  # Estamos inserindo na variável receitas tudo aquilo que se encontra no bloco representado pela classe "recipe-card".
  # O primeiro parâmetro, "div", sinaliza que se trata de um dos blocos/divisões da página em questão. 
  # O segundo informa a classe que classifica essa divisão.
  receitas = categoria_html.find_all('div', class_="recipe-card")
  # Para cada uma das receitas encontradas:
  for r in receitas:
    # Printamos o elemento de texto classificado por "recipe-title".
    print("\t\t",str(r.find('h4',class_="recipe-title").text).replace("\n",""))
    # Printamos todas as tags de classe "row".
    print(str(r.find('a',class_="row")['href']))
  print("\n")


# # Paginas por Categoria

# In[7]:


# Para cada uma das categorias existentes:
for i in categorias:
  print(i.text,':',)
  # Estamos fazendo a requisição da página que contém todas as receitas daquela categoria. 'href' é o texto "em url" que
  # especifica a categoria em questão.
  categoria = request_pag(url+i['href']) #Requisitando a pagina da categoria
  # Estamos instanciando um objeto BeautifulSoup com a página retornada pela requisição para que possemos extrair os dados
  # desejados.
  categoria_html = BeautifulSoup(categoria, 'lxml')
  # Criando uma lista vazia.
  pag_visitadas= []
  # Encontrando na divisão da página especificada pela classe "pagination" todas as tags de classe "row".
  paginas = categoria_html.find('div', class_="pagination").find_all(class_='row')
  pagina_atual = 1
  # Para todas as páginas existentes
  for pag in paginas:
    # Caso encontremos um span de classe "current"
    if pag.find("span",class_="current"):
      pagina_atual = int(pag.span.text)
  #break


# # Scraping dados de uma Receita

# Informações Iniciais

# In[8]:


# Estamos fazendo a requisição da página que contém a receita desejada.
receita = request_pag("https://www.tudogostoso.com.br/receita/47884-esfiha-de-carne-adaptada-receita-turca.html")
# Estamos instanciando um objeto BeautifulSoup com a página retornada pela requisição para que possemos extrair os dados
# desejados.
receita_html = BeautifulSoup(receita, 'lxml')


# Tempo de Preparo:

# In[9]:


# Encontrando informações sobre a tag "time"
tempo_de_preparo = receita_html.find('time' )
# Utilizamos o .text para representar o conteúdo contido em tempo_de_preparo
print("Tempo de Preparo:",tempo_de_preparo.text.replace("\n",""))


# Rendimento:

# In[10]:


# Encontrando informações sobre a propriedade "recipeYield" do item.
rendimento = receita_html.find(itemprop="recipeYield")
# Utilizamos o .text para representar o conteúdo contido em tempo_de_preparo
print("Rendimento:",rendimento.text.replace("\n",""))


# Ingredientes:

# In[11]:


# Encontrando todas as informações existentes na divisão da página receita_html classificada por "ingredients-card".
ingredientes_html = receita_html.find_all('div', class_="ingredients-card")

# Para cada um dos ingredientes:
for i in ingredientes_html:
  ingredientes = i.find_all(["li", "h3"])
  for ingrediente in ingredientes:
    # Utilizamos o .text para representar o conteúdo textual contido em ingrediente.
    print(ingrediente.text)


# Modo de Preparo

# In[12]:


# Encontrando todas as informações existentes na divisão da página receita_html classificada por "instructions".
preparo_html = receita_html.find('div', class_="instructions")

preparo = str(preparo_html).replace("</li>","\n")
preparo = preparo.replace("<li>","")
preparo = preparo.replace("<ol>","")
preparo = preparo.replace('<span tabindex="0">',"")
preparo = preparo.replace('<div class="instructions e-instructions" itemprop="recipeInstructions">',"")
preparo = preparo.replace('</ol>\n</div>]',"")
preparo = preparo.replace('<h3 class="card-subtitle">',"\n")
preparo = preparo.replace('</h3>',"\n")
preparo = preparo.replace('</ol>',"")
preparo = preparo.replace('</span>',"")

print(preparo)


# # Automatização do scrapping

# In[13]:


#ENTRAR NA PAGINA INICIAL utilizando os pages 
url = "https://www.tudogostoso.com.br"

pag_inicial = request_pag(url)
pag_inicial_html = BeautifulSoup(pag_inicial, 'lxml')

base_de_dados = {"receita":[],"ingredientes":[],"preparo":[],"tempo_de_preparo":[],"rendimento":[],"categoria":[]}


#Ir nas seções de tipos de receitas
categorias = pag_inicial_html.find_all('a',class_='category-item')

for c in categorias:
  cat_link = url+c['href']
  cat_nome = str(c.text)
  print("Categoria: ",cat_nome)
  categoria = request_pag(cat_link) 
  secao = BeautifulSoup(categoria, 'lxml')
  receitas = secao.find_all('div', class_="recipe-card")
  #Pegar as receitas da seção
  for r in receitas:
    titulo = str(r.find('h4',class_="recipe-title").text).replace("\n","")
    
    receita_link = str(r.find('a',class_="row")['href'])

    receita_html = request_pag(url+receita_link)

    receita = BeautifulSoup(receita_html, 'lxml')

    ingredientes_html = receita.find_all('div', class_="ingredients-card")
    ingredientes_str = ""
    
    #Pegando os ingredientes da receita
    for i in ingredientes_html:
      ingredientes = i.find_all(["li", "h3"])
      for ingrediente in ingredientes:
        ingredientes_str += str(ingrediente.text)+"\n"
    
    #pegando o modo de preparo
    preparo_html = receita.find('div', class_="instructions")
    preparo = str(preparo_html).replace("</li>","\n")
    preparo = preparo.replace("<li>","")
    preparo = preparo.replace("<ol>","")
    preparo = preparo.replace('<span tabindex="0">',"")
    preparo = preparo.replace('<div class="instructions e-instructions" itemprop="recipeInstructions">',"")
    preparo = preparo.replace('</ol>\n</div>]',"")
    preparo = preparo.replace('<h3 class="card-subtitle">',"\n")
    preparo = preparo.replace('</h3>',"\n")
    preparo = preparo.replace('</ol>',"")
    preparo = preparo.replace('<p>',"")
    preparo = preparo.replace('</p>',"")
    preparo = preparo.replace('</div>',"")
    preparo = preparo.replace('</strong>',"")
    preparo = preparo.replace('<strong>',"")
    preparo = preparo.replace('</span>',"")
    
    
    #Informacoes da receita
    tempo_de_preparo = receita.find('time').text.replace("\n","")
    rendimento = receita.find(itemprop="recipeYield").text.replace("\n","")

    
    #Adicionando na lista
    base_de_dados["receita"].append(titulo)
    base_de_dados["ingredientes"].append(ingredientes_str)
    base_de_dados["preparo"].append(preparo)
    base_de_dados["tempo_de_preparo"].append(tempo_de_preparo)
    base_de_dados["rendimento"].append(rendimento)
    base_de_dados["categoria"].append(cat_nome)
    #break


# # DataFrame

# Criando um DataFrame com a base de dados construida

# In[14]:


import pandas as pd

df_receitas = pd.DataFrame(data=base_de_dados)

print(len(df_receitas))
df_receitas.head()

