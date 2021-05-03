# import bibliotecas
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from parsel import Selector
import csv

# instanciar arquivo csv
arquivo = csv.writer(open('output.csv', 'w', encoding='utf-8'))
arquivo.writerow(['Nome', 'Headline', 'URL'])

# a. objeto do tipo navegador
navegador = webdriver.Chrome('E:/Portifolio/Scraping/chromedriver')
sleep(1)

# a.1 maximizamos o navegador
#navegador.maximize_window()

# b. acesso as páginas html
navegador.get('http://www.linkedin.com/')

# Cada página HTML terá sua própria arquitetura de construção. As tag's e os on nossos objetivos
# que orientará o pipeline que contruiremos!!!!

# c. logando
navegador.find_element_by_xpath('//a[text()="Entrar"]').click()
sleep(3)

# d.
# d.1 usuário -> a tag possui atributo "name = 'session_key'"
usuario = navegador.find_element_by_name('session_key')

# d.1.1
usuario.send_keys('seuemail@seuemail.com')

# d.2
senha = navegador.find_element_by_name('session_password')

# d.2.1
#senha.send_keys(input())
senha.send_keys('testescript')

# d.3
senha.send_keys(Keys.ENTER)
sleep(3)

# Lembrar dados Navegador: como é didatico não vou salvar
#navegador.find_element_by_xpath('//button[text()= "Agora não"]').click()

#------------------------------------- logamos no linkedIn ------------------------------------------------------------#

# e. Acessando engine de busca
navegador.get('http://www.google.com')
sleep(1)

# e.1
buscador = navegador.find_element_by_name('q')

# e.2 critérios de busca
buscador.send_keys('site:linkedin.com/in AND "cientista de dados" AND "Banco do Brasil"')
sleep(2)

# e.3 Enter para realizar a busca
buscador.send_keys(Keys.ENTER)

# f. (output: uma lista de elementos da classe passada como parametro, endereçada)
lista_perfil= navegador.find_elements_by_xpath('//div[@class= "yuRUbf"] /a')

# g. (output: lista apenas com links)
lista_perfil = [perfil.get_attribute('href') for perfil in lista_perfil]

# acessamos o link do 1° elemento da lista
# navegador.get(lista_perfil[0])

# h. iteração com cada link da lista
for perfil in lista_perfil:
    navegador.get(perfil)
    sleep(4)

    raspador = Selector(text= navegador.page_source)
    nome = raspador.xpath('//title/text()').extract_first().split(' | ')[0]
    headline = raspador.xpath('//h2/text()')[2].extract().strip()
    url = navegador.current_url

    arquivo.writerow([nome, headline, url])

    # conectar com esse perfil:
    navegador.find_element_by_xpath('//span[text()="Conectar"]').click()

    # i. posso adicionar nota
    navegador.find_element_by_xpath('//span[text()="Adicionar nota"]').click()
        # acesso elemento unico
    mensagem = navegador.find_element_by_name('message')
    mensagem.send_keys('obrigado por me adicionar!! https://github.com/angeloBuso/scraping_perfil')
    navegador.find_element_by_xpath('//span[text()="Enviar"]').click()

    # ii. apenas conectar
    #navegador.find_element_by_xpath('//span[text()="Enviar"]').click()


navegador.quit()




