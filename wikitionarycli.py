from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup, SoupStrainer

webpage = 'https://www.wiktionary.org/'
ch = 'y'

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
  url = driver.current_url #finding current url after submitting input

  if url.find('Special') == -1 :
    r = requests.get(url)
    soup = BeautifulSoup(r.text , 'lxml')
    print(soup.find('h1',{'id':'firstHeading'}).text)
    l = ['Noun','Conjunction','Verb','Article','Adverb','Pronoun','Adjective','Preposition','Interjection']

    for i in l:
     if soup.find('span',{'id':i}) != None :
         print()
         print(soup.find('span',{'id':i}).text)
         print()
         print(soup.find('span',{'id': i}).find_next('ol').li.text)     
    


  else :
    print('No such word found!')
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    print("Related words:")
    for i in soup.find_all('li',{'class':'mw-search-result'}):
      print(i.div.text)


  ch = input('Wanna search again? y/n :')