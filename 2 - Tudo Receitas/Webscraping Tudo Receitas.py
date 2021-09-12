#!/usr/bin/env python
# coding: utf-8

# # Bibliotecas Necessárias

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup


# # Requisitando Página

# In[2]:


def request_pag(link):
    html = requests.get(link)
    
    return html.text


# In[3]:


request_pag("https://www.tudoreceitas.com/")


# # BeautifulSoup

# In[4]:


# URL
url = "https://www.tudoreceitas.com/"

# lendo a URL 
html = requests.get(url)

# Instanciando um Objeto BeautifulSoup
bs = BeautifulSoup(html.text, 'lxml')

# Imprimindo o título da página
print(bs.title)


# # Categorias de Receitas

# Primeiro Método

# In[5]:


# Encontrando todas as categorias (todas as tags a de classe "titulo"):
cat = bs.find_all('a', class_='titulo')

# Filtrando as categorias
categorias = []
for i in cat:
  # Estamos filtrando pelo texto para contornar as incossistências na decumentação.
  if( ("Receitas" in i.text) | ("Coquetéis" in i.text)):
        categorias.append(i)
        
# Para todas as categorias:
for i in categorias:
  # Printamos o texto "em url" que especifica a categoria em questão.
  #if( ("Receitas" in i.text) | ("Coquetéis" in i.text)):
      print(i.text,"->",i['href'],'\n')


# Segundo Método

# In[6]:


# Encontrando todas as categorias:
categorias = bs.find_all('div', class_="categoria ga")

# Para cada uma das categorias:
for categoria in categorias:
    print(categoria['data-label'], ":")
    print(categoria.find("a")['href'])


# # Receitas por Categoria

# In[7]:


# Encontrando todas as categorias (todas as tags a de classe "titulo"):
cat = bs.find_all('a', class_='titulo')

# Filtrando as categorias
categorias = []
for i in cat:
  # Estamos filtrando pelo texto para contornar as incossistências na decumentação.
  if( ("Receitas" in i.text) | ("Coquetéis" in i.text)):
        categorias.append(i)
        
# Para cada uma das categorias existentes:
for i in categorias:
  print(i.text,':')
  # Estamos fazendo a requisição da página que contém todas as receitas daquela categoria. 'href' é o texto "em url" que
  # especifica a categoria em questão.
  categoria = request_pag(i['href'])
  # Estamos instanciando um objeto BeautifulSoup com a página retornada pela requisição para que possemos extrair os dados
  # desejados.
  categoria_html = BeautifulSoup(categoria, 'lxml')

  # Estamos inserindo na variável receitas tudo aquilo que se encontra no bloco representado pela classe "titulo titulo
  # --resultado".
  # O primeiro parâmetro, "a", sinaliza que se trata de um dos links da página em questão. 
  # O segundo informa a classe que classifica essa divisão.
  receitas = categoria_html.find_all('a', class_="titulo titulo--resultado")
  print("Quantidade de receitas: ", len(receitas), "\n")

  # Para cada uma das receitas encontradas:
  for r in receitas:
    # Printamos o nome da receita e sua respectiva página web.
    print(r.text, ": ", r['href'], "\n")
  print("\n")


# # Coletando os Dados de uma Receita

# Informações iniciais

# In[8]:


# Estamos fazendo a requisição da página que contém a receita desejada.
receita = request_pag("https://www.tudoreceitas.com/receita-de-pao-de-alho-caseiro-com-queijo-9344.html")
# Estamos instanciando um objeto BeautifulSoup com a página retornada pela requisição para que possemos extrair os dados
# desejados.
receita_html = BeautifulSoup(receita, 'lxml')


# Tempo de preparo

# In[9]:


# Encontrando informações sobre a tag "duracion"
tempo_de_preparo = receita_html.find("span", class_="property duracion")
# Utilizamos o .text para representar o conteúdo contido em tempo_de_preparo
print("Tempo de Preparo:",tempo_de_preparo.text.replace("\n",""))


# Rendimento

# In[10]:


# Encontrando informações sobre a propriedade "comensales" do item.
rendimento = receita_html.find("span", class_="property comensales")
# Utilizamos o .text para representar o conteúdo contido em tempo_de_preparo
print("Rendimento:",rendimento.text.replace("\n",""))


# Para

# In[11]:


# Encontrando informações sobre a propriedade "para" do item.
para = receita_html.find("span", class_="property para")
# Utilizamos o .text para representar o conteúdo contido em tempo_de_preparo
print("Para:",para.text.replace("\n",""))


# Dificuldade

# In[12]:


# Encontrando informações sobre a propriedade "property dificultad" do item.
dificuldade = receita_html.find("span", class_="property dificultad")
# Utilizamos o .text para representar o conteúdo contido em tempo_de_preparo
print("Para:", dificuldade.text.replace("\n",""))


# Imagem

# In[13]:


# Encontrando informações sobre a propriedade "imagen lupa" do item.
imagem = receita_html.find("div", class_="imagen lupa")
# Utilizamos o .text para representar o conteúdo contido em tempo_de_preparo
print("Imagem: ", imagem.find('img')['src'])


# Ingredientes

# In[14]:


# Encontrando todas as informações existentes na divisão da página receita_html classificada por "ingredientes".
ingredientes_html = receita_html.find_all('div', class_="ingredientes")

# Para cada um dos ingredientes:
for i in ingredientes_html:
  ingredientes = i.find_all("li")
  for ingrediente in ingredientes:
    # Utilizamos o .text para representar o conteúdo textual contido em ingrediente.
    print(ingrediente.text)


# Modo de Preparo

# In[15]:


# Encontrando todas as informações existentes na divisão da página receita_html classificada por "instructions".
preparo_html = receita_html.find_all('div', class_="apartado")

preparo = ""

# Para cada um dos passos de preparo:
for i in preparo_html:
    passos = i.find("p")
    for passo in passos:
        # Utilizamos o .text para representar o conteúdo textual contido em ingrediente.
        preparo = preparo + str(passo)

print(preparo)


# # Automatização do Scraping

# In[16]:



# Criando na página inicial utilizando os pages 
url = "https://www.tudoreceitas.com/"

pag_inicial = request_pag(url)
pag_inicial_html = BeautifulSoup(pag_inicial, 'lxml')

# Criando a base de dados
base_de_dados = {"receita":[],"ingredientes":[],"preparo":[],"tempo_de_preparo":[],"rendimento":[],"serve_como":[],
                 "dificuldade":[],"imagem":[],"categoria":[]}

# Indo nas seções de tipos de receitas
cat = bs.find_all('a', class_='titulo')

# Filtrando as categorias
categorias = []
for i in cat:
    # Estamos filtrando pelo texto para contornar as incossistências na decumentação.
    if( ("Receitas" in i.text) | ("Coquetéis" in i.text)):
        categorias.append(i)

print("Categorias Concluídas:\n")

for categoria in categorias:
    # Requisitando a página da categoria
    categoria_html = request_pag(categoria['href']) 
    secao = BeautifulSoup(categoria_html, 'lxml')
  
    # Requisitando as receitas daquela secao/categoria
    receitas = secao.find_all('a', class_="titulo titulo--resultado")
    
    for receita in receitas:
        # Requisitando a página da receita:
        receita_html = request_pag(receita['href'])
        receita_bs = BeautifulSoup(receita_html, 'lxml')
        
        # Título da Receita:
        Titulo = receita.text
        
        # Ingrediantes da Receita:
        ingredientes_html = receita_bs.find_all('div', class_="ingredientes")
        Ingredientes = ""
        # Para cada um dos ingredientes:
        for i in ingredientes_html:
            ingreds = i.find_all("li")
        for ingrediente in ingreds:
            # Utilizamos o .text para representar o conteúdo textual contido em ingrediente.
            Ingredientes += str(ingrediente.text)
        
        # Modo de Preparo da Receita:
        preparo_html = receita_bs.find_all('div', class_="apartado")

        Preparo = ""

        # Para cada um dos passos de preparo:
        for i in preparo_html:
            passos = i.find_all("p")
            for passo in passos:
                # Utilizamos o .text para representar o conteúdo textual contido em ingrediente.
                Preparo = Preparo + str(passo.text)
                
        # Tempo de Preparo:
        if(receita_bs.find("span", class_="property duracion") == None):
            Tempo = "--"
        else:
            Tempo = receita_bs.find("span", class_="property duracion").text
        
        # Rendimento:
        if(receita_bs.find("span", class_="property comensales") == None):
            Rendimento = "--"
        else:
            Rendimento = receita_bs.find("span", class_="property comensales").text
        
        # Serve como:
        if(receita_bs.find("span", class_="property para") == None):
            Serve = "--"
        else:
            Serve = receita_bs.find("span", class_="property para").text
        
        # Dificuldade:
        if(receita_bs.find("span", class_="property dificultad") == None):
            Dificuldade = "--"
        else:
            Dificuldade = receita_bs.find("span", class_="property dificultad").text
        
        # Imagem:
        Imagem = receita_bs.find("div", class_="imagen lupa").find('img')['src']
        
        # Categoria:
        Categoria = categoria.text
        
        #Adicionando na Base de Dados
        base_de_dados["receita"].append(Titulo)
        base_de_dados["ingredientes"].append(Ingredientes)
        base_de_dados["preparo"].append(Preparo)
        base_de_dados["tempo_de_preparo"].append(Tempo)
        base_de_dados["rendimento"].append(Rendimento)
        base_de_dados["serve_como"].append(Serve)
        base_de_dados["dificuldade"].append(Dificuldade)
        base_de_dados["imagem"].append(Imagem)
        base_de_dados["categoria"].append(Categoria)
        
    print(categoria.text, "\n")


# # Criando a Base de Dados

# In[17]:


df_receitas = pd.DataFrame(data = base_de_dados)
df_receitas


# # Exportando a Base de Dados

# In[19]:


df_receitas['categoria'].value_counts()


# In[20]:


df_receitas.to_csv('C:\\Users\\LENOVO\\Desktop\\UFPI\\Projeto Webscraping\\Bases\\Tudo_Receitas.csv')

