from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup

webpage = 'https://www.wiktionary.org/'
ch = 'y'


#The following lines are for input



while ch == 'y' :
  
  driver = webdriver.Firefox()
  driver.get(webpage)
  langlist = driver.find_element_by_id('searchLanguage') #language drop box element

  options = [ x for x in langlist.find_elements_by_tag_name('option')]
  
  print('List of languages:')

  for option in options :
      print(option.text)
  
  language = input('Enter the language from the list above (exactly as in list):')
  dropdown = Select(langlist)
  dropdown.select_by_visible_text(language)#selecting the language option

  searchterm= input('Enter the word to be searched:')
  sbox = driver.find_element_by_name('search')
  sbox.send_keys(searchterm)  #putting the input in the search box

  submit = driver.find_element_by_name('go')
  submit.click()  #clicking the submit button

  assert "No results found" not in driver.page_source 


  #The following lines are for output


  url = driver.current_url #finding current url after submitting input
  print('\n\n')

  r = requests.get(url)
  soup = BeautifulSoup(r.text , 'lxml')

  #Printing the meanings
  if url.find('Special') == -1 :
    
    print(soup.find('h1',{'id':'firstHeading'}).text)
    print('\n\n')
    l = ['Noun','Conjunction','Verb','Article','Adverb','Pronoun','Adjective','Preposition','Interjection']

    for i in l:
     if soup.find('span',{'id':i}) != None :
         print()
         print(soup.find('span',{'id':i}).text)
         print()
         for j in soup.find('span',{'id': i}).find_next('ol').find_all('li'):
           print (j.text)    
    


  else :
    print('No such word found!')
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    print("Related words:")
    for i in soup.find_all('li',{'class':'mw-search-result'}):
      print(i.div.text)

  print()

  ch = input('Wanna search again? y/n :')