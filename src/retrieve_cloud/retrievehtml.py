import requests
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

# movie name must follow letterboxd username format
moviename = input('Enter Movie Name:')
pagenumber = input('Enter Maximum Page Number:')
URL = f"https://letterboxd.com/film/{moviename}/reviews/by/activity/"

if pagenumber !='':
	try:
		maxpagenumber = int(pagenumber)
	except:
		print('Invalid Number')
		quit()

# selenium environment
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--headless')
options.add_argument('--log-level=2')
driver = webdriver.Chrome(options=options)


# print(page.content)
while True:
	driver.get(URL) # selenium
	page = requests.get(URL) # requests
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find(id="content") # site section
	try:
		reviews = results.find_all("div", class_="film-detail-content") # each review block
	except:
		print("Invalid Name")
		quit()	
	reviews_list = []
	for review in reviews:
		review_body = review.find("div", class_="body-text -prose collapsible-text") 
		linksuffix = review_body['data-full-text-url'] # suffix of full text url to concat
		link = "https://letterboxd.com" + linksuffix
		reviewpage = requests.get(link) # set up new soup for link url
		reviewsoup = BeautifulSoup(reviewpage.content, "html.parser")
		reviews_list.append(reviewsoup.get_text()) # append to list just text from reviews

	try:
		driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content']/div/div/section/section/div/div[2]/a"))))
		driver.find_element(By.XPATH, "//*[@id='content']/div/div/section/section/div/div[2]/a").click()
		URL = driver.current_url # switch to next page
		if pagenumber !='':
			if URL == f"https://letterboxd.com/film/{moviename}/reviews/by/activity/page/{maxpagenumber}/":
				print('Done')
				break
	except TimeoutException:
		print('Finished')
		break

# readable list with no /n
convert_list = []
for r in reviews_list:
	convert_list.append(r.strip())
wc = ''.join(convert_list)

# plot wordcloud
def plot_cloud(wordcloud):
	plt.figure(figsize=(40, 30))
	plt.imshow(wordcloud)
	plt.axis("off")

mask = np.array(Image.open('camera.png')) # local image reference

# additional stop words in different languages
stopword_lang = ["c'est",'alors',"j'??tais",'??','acune','algo','au','de','aucun','juste','sujet','??ltimo','estar??','podia','un','desde','cierto','lo','empleas','die'
'au','la','sur','??','este','por','una','conseguir','ciertos','las','emplean','dies'
'aucuns','le','ta','acerca','estes','porque','unas','consigo','cierta','los','ampleamos','dieser'
'aussi','les','tandis','agora','esteve','povo','unos','consigue','ciertas','su','empleais','dieses'
'autre','leur','tellement','algmas','estive','promeiro','uno','consigues','intentar','aqui','valor','doch'
'avant','l??','tels','alguns','estivemos','qu??','sobre','conseguimos','intento','mio','muy','dort'
'avec','ma','tes','ali','estiveram','qual','todo','consiguen','intenta','tuyo','era','du'
'avoir','maintenant','ton','ambos','eu','qualquer','tambi??n','ir','intentas','ellos','eras','durch'
'bon','mais','tous','antes','far??','quando','tras','voy','intentamos','ellas','eramos','ein'
'car','mes','tout','apontar','faz','quem','otro','va','intentais','nos','eran','eine'
'ce','mien','trop','aquela','fazer','quieto','alg??n','vamos','intentan','nosotros','modo','einem'
'cela','moins','tr??s','aquelas','fazia','s??o','alguno','vais','dos','vosotros','bien','einen'
'ces','mon','tu','aquele','fez','saber','alguna','van','bajo','vosotras','cual','einer'
'ceux','mot','voient','aqueles','fim','sem','algunos','vaya','arriba','si','cuando','eines'
'chaque','m??me','vont','aqui','foi','ser','algunas','gueno','encima','dentro','donde','er'
'ci','ni','votre','atr??s','fora','seu','ser','ha','usar','solo','mientras','es'
'comme','nomm??s','vous','bem','horas','somente','es','tener','uso','solamente','quien','euer'
'comment','notre','vu','bom','iniciar','t??m','soy','tengo','usas','saber','con','eure'
'dans','nous','??a','cada','inicio','tal','eres','tiene','usa','sabes','entre','f??r'
'des','ou','??taient','caminho','ir','tamb??m','somos','tenemos','usamos','sabe','sin','hatte'
'du','o??','??tat','cima','ir??','tem','sois','teneis','usais','sabemos','trabajo','hatten'
'dedans','par','??tions','com','ista','tempo','estoy','tienen','usan','sabeis','trabajar','hattest'
'dehors','parce','??t??','como','iste','tenho','esta','el','emplear','trabajan','zum','hattet'
'depuis','pas','??tre','comprido','isto','tentar','estamos','la','empleo','podria','zur','hier'
'devrait','peut','aber','hinter','unsere','conhecido','ligado','tentaram','estais','podrias','??ber','sollt'
'doit','peu','als','ich','unter','corrente','maioria','tente','estan','haces','hacemos','sonst'
'donc','plupart','am','ihr','vom','das','maiorias','tentei','como','muchos','haceis','soweit'
'dos','pour','an','ihre','von','debaixo','mais','teu','en','aquellos','hacen','sowie'
'd??but','pourquoi','auch','im','vor','dentro','mas','teve','para','podriamos','cada','und'
'elle','quand','auf','in','wann','desde','mesmo','tipo','atras','podrian','fin','unser'
'elles','que','aus','ist','warum','desligado','meu','tive','porque','podriais','incluso',
'en','quel','bei','ja','was','deve','muito','todos','por qu??','yo','primero',
'encore','quelle','bin','jede','weiter','devem','muitos','trabalhar','estado','aquel','musst',
'essai','quelles','bis','jedem','weitere','dever??','n??s','trabalho','estaba','hacer','m??ssen',
'est','quels','bist','jeden','wenn','direita','n??o','tu','ante','hago','m????t',
'et','qui','da','jeder','wer','diz','nome','um','antes','hace','nach',
'eu','sa','dadurch','jedes','werde','dizer','nosso','uma','siendo','aquellas','nachdem',
'fait','sans','daher','jener','werden','dois','novo','umas','ambos','sus','nein',
'faites','ses','darum','jenes','werdet','dos','o','uns','pero','entonces','nicht',
'fois','seulement','das','jetzt','weshalb','e','onde','usa','por','tiempo','nun',
'font','si','da??','kann','und','eine','seiner','mir','steht','bilder','bildern','zwei','geht',
'h??tte','w??re','habe','die','diese','dann','alle','haben','allem','immer','geschehen','einen','geht','pi??','ganz','zwar','wie','ela','os','usar','poder','verdad','oder',
'hors','sien','dass','kannst','wieder','ele','ou','valor','puede','verdadero','seid',
'ici','son','dein','k??nnen','wieso','eles','outro','veja','puedo','verdadera','sein',
'il','sont','deine','k??nnt','wir','wurde','anche','viele','durch','f??r','em','para','ver','podemos','zum','seine',
'ils','sous','dem','machen','wird','enquanto','parte','verdade','podeis','zur','sich',
'je','soyez','den','mein','wirst','ent??o','pegar','verdadeiro','pueden','??ber','sie',
'der','meine','wo','est??','pelo','voc??','fui','saben','trabajas','hacemos','sind',
'des','mit','woher','est??o','pessoas','fue','ultimo','trabaja','fin','haceis','soll',
'dessen','mu??','wohin','estado','pode','fuimos','largo','trabajamos','incluso','hacen','sollen',
'deshalb','mu??t','zu','estar','poder??','fueron','bastante','trabajais','primero','cada','sollst','much'] + list(STOPWORDS)

# generate word cloud
wordcloud = WordCloud(width= 3000, height = 2000, random_state=1, background_color='white', colormap='RdYlGn', collocations=False, stopwords = stopword_lang, mask=mask, min_word_length= 3).generate(wc)
plot_cloud(wordcloud)
wordcloud.to_file("wordcloud.png") # local save file