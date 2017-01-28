import urllib.request
import os
from bs4 import BeautifulSoup
#CREATO DA DIEGO PORTOGHESE
#I dati recuperati mediante questo software sono al solo scopo didattico
#Non mi prendo nessuna responsabilità del utilizzo illecito di questo software da terze partiti
#	www.musicstoreitalia.com
website = urllib.request.urlopen("http://www.musicstoreitalia.com")
data=website.read()


class Product:
	def __init__(self,id_,name_, link_, category_name_,price_,comment_):
		self.id=id_
		#basic % 
		os.system('cls' if os.name == 'nt' else 'clear')
		float=self.id/2400
		print("Loading: ",int(float*100),"%") 
		# FIX and Casting
		name_=name_.replace(u'\u2033', '"')
		name_=name_.replace(';','')
		name_=name_.replace('\n','')
		self.name=name_
		self.link=link_
		category_name_=category_name_.replace('\n','')
		category_name_=category_name_.replace(';','')
		self.category_name=category_name_
		price_=price_.replace('€','')
		price_=price_.replace(' ','')
		price_=price_.replace(',','.')
		price_=price_.replace('\n','')
		price_=price_.replace(';','')
		price_=price_.replace('\u2033', '"')
		self.price=price_
		comment_=comment_.replace('\n','')
		comment_=comment_.replace(';','')
		self.comment=comment_
		'''
		immagelink
		'''
	def printProduct(self):
		#without comment IT IS GOOD
		return ""+str(self.id)+";"+self.name+";"+self.link+";"+self.category_name+";"+self.price+"\n"
		#with comment 
		#return " "+str(self.id)+";"+self.name+";"+self.link+";"+self.category_name+";"+self.price+";"+self.comment+"\n"
		
id=0
product_=[]
out_file = open("test.csv","w")

#Take the products link From Category page
def GetProductsFromCategory(category_link,category_name,i):

	if i != 0:
		CategoryLink = urllib.request.urlopen(category_link)
		dataCategory=CategoryLink.read()
		CategorySoup = BeautifulSoup(dataCategory, 'html.parser')
		
		for divproduct in CategorySoup.find_all("ol",{"class":"products-list"}):
			for info in divproduct.find_all("div",{"class":"product-shop"}):
				global id
				
				h2_=info.h2#name and link
				links=h2_.find_all('a', href=True)
				
				#for special price
				sprice=str(info.find_all('p', {'class':'special-price'} ) )
				spriceT=sprice.replace(' ','')
				#Special Price
				if spriceT != '[]':
					for span in info.find_all('p', {'class':'special-price'} ):
						for idspan in span.find_all("span",id=True):
							price=idspan.text
				#price Normal	
				else:
					pricebox=info.find_all('div', {'class':'price-box'})
					price=pricebox[0].span.text
				
				com_=info.find_all('div',{'class':'desc std'})#comment
				#Send all Info to class Product
										#id		#name	#link					#category		#price				#comment
				product_.append(Product(id, h2_.string, links[0].attrs['href'], category_name, price, com_[0].text))
				#write inside the file
				out_file.write(product_[id].printProduct())
				id+=1
			
		#next page (in div toolbar-bottom)
		for li in CategorySoup.find_all("div", {"class":"toolbar-bottom"}):
			#Casting of " [] " to "" (because i have a problem with this)
			x=str(li.find_all("a", {"class":"next i-next"}))
			if x.replace(" ","") != "[]":
				
				#print("",li.find_all("a", {"class":"next i-next"}),"")#for debug
				for href in li.find_all("a", {"class":"next i-next"}):
					#Recorsive Function ()
					GetProductsFromCategory(href.get("href"),category_name,i)
			else:
				#no more page
				return
				
		
			#print( li.find_all("a", {"class":"next i-next"}) )
				
	
#						Category 
category_list = []
category_nameB = []
category_name = []
category_n=0
blockcontent = BeautifulSoup(data, 'html.parser')
for a in blockcontent.find_all("div", {"class":"block-content"}):
	for link in a.find_all('a'):
		#print(link.get('href')) #fore debug
		category_list.append(link.get('href'))
		category_nameB.append(link.get_text())
		category_n+=1
#casting category_name ('\n') 
for category in category_nameB:
	category_name.append(category.replace('\n', ''))

i=0
for category in category_list:
	GetProductsFromCategory(category_list[i],category_name[i],i) #START FUNCION
	i+=1
	
	
print("Finish, test.csv created")
out_file.close