import urllib.request
import os

from datetime import datetime
from selenium import webdriver
from operator import itemgetter
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from ncore_category_dict import ncore_category_dictionary


class nCore(object):
	"nCore search implementation class."

	__ncore_url = "https://ncore.cc"
	
	def __init__(self, uname, passwd):
		__options = Options()
		__options.add_argument("--headless")
		#self._webdriver = webdriver.Firefox(firefox_options=__options, 
		#	executable_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "pack/geckodriver"))
		self._webdriver = webdriver.PhantomJS(
			os.path.join(os.path.dirname(os.path.realpath(__file__)), "pack/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"))

		self._webdriver.get(self.__ncore_url + "/login.php")

		username = self._webdriver.find_element_by_name("nev")
		password = self._webdriver.find_element_by_name("pass")
		
		submit_button = self._webdriver.find_element_by_class_name("submit_btn")

		username.send_keys(uname)
		password.send_keys(passwd)

		submit_button.submit()

		with open("/home/pityu/Asztal/page.html", "w") as fout:
			fout.write(self._webdriver.page_source)

	def __category_check(self, category):
		if not category or not isinstance(category, dict):
			return

		for catname in category.keys():
			main = ncore_category_dictionary.get(catname, None)
			if main:
				fo_resz = self._webdriver.find_element_by_name(main.get("name", None))
				if not fo_resz:
					print("Nem talaltam ilyet: {0}[name].".format(catname))
					continue
				
				fo_resz.click()

				for sub in category.get(catname):
					sub_chances = main.get("chances", None)
					if not sub_chances:
						print("Nem talaltam 'chances'-t.")
						continue
					
					sub_actual = sub_chances.get(sub, None)
					
					if not sub_actual:
						print("Nem talaltam meg: {0} a chances-ban.".format(sub))
						continue

					sub_resz = self._webdriver.find_element_by_id(sub_actual)

					if not sub_resz:
						print("Nem talaltam ilyet: {0}".format(sub_resz))
						continue

					sub_resz.click()
			else:
				print("Nincs ilyen a szotarban: {0}".format(catname))

	def search(self, search, category=None):
		self._webdriver.get(self.__ncore_url + "/torrents.php")
		
		# Beklikkelgetjuk, ha van kategoria megadva.
		if category:
			self.__category_check(category)

		kereso_mezo = self._webdriver.find_element_by_id("mire")
		kereso_mezo.send_keys(search)
		submit_button = self._webdriver.find_element_by_name("submit")
		submit_button.submit()
		
		href_search_xpath = "//a[@href and contains(translate(@title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{0}')]".format(search.lower())
		result = list()
		date_array = self._webdriver.find_elements_by_class_name("box_feltoltve2")
		link_array = self._webdriver.find_elements_by_xpath(href_search_xpath)

		for tmp in zip(date_array, link_array):
			result.append(
				{
					"cim": tmp[1].get_attribute("title"),
					"link": tmp[1].get_attribute("href"),
					"datum": datetime.strptime(tmp[0].text.replace("\n", " "), "%Y-%m-%d %H:%M:%S") #2017-03-22 23:51:51
				}
			)
		return sorted(result, key=itemgetter('datum'), reverse=True)

	def download(self, *args, **kwargs):
		"Download the specified page."
		prev_link = self._webdriver.current_url			# Elmentem kesobbre
		self._webdriver.get(kwargs.get("link"))

		download_link = self._webdriver.find_element_by_xpath(".//div[@class='download']/a")
		print(download_link.get_attribute("href"))

		local_file_name = "/tmp/{0}.{1}".format(kwargs.get("cim").replace(" ","_"), "torrent")

		urllib.request.urlretrieve(
			download_link.get_attribute("href"), 
			local_file_name
			)

		self._webdriver.get(prev_link)			# Visszamegyek oda, ahol voltam belepeskor.
		return local_file_name
