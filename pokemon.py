import numpy as np
import requests, shelve, bs4, time, pprint

class Pokemon():
	def __init__(self):
		self.data_preprocess()

	def data_collect(self):
		sh = shelve.open("pokemon")

		data = []
		for i in range(1, 807):
			print("Wating...")
			time.sleep(2)
			try:
				url = "https://yakkun.com/sm/zukan/n" + str(i)

				response = requests.get(url)
				response.encoding = response.apparent_encoding
				response.raise_for_status()

				sp = bs4.BeautifulSoup(response.text,"html.parser")

				name_table = sp.select('table[summary="基本データ"]')[0]
				name = name_table.select('th')[0].text

				type_ul = sp.select('ul[class="type"]')[0]
				types_li = type_ul.select('li')
				types = tuple(tp.select('img')[0]["alt"] for tp in types_li)

				tbody = sp.select('table[class="center"]')[0]

				status = [x for x in map(lambda s: (s[0], int(s[1])), [[td.text for td in tr.select('td')] for tr in tbody.select("tr")][1:7])]

				data.append(dict(zip(["name", "num", "types", "status"],[name, i, types, status])))
			except:
				print("error", str(i))

		print(data)
		sh["pokemon"] = data

	def data_preprocess(self):
		sh = shelve.open("pokemon")
		data = sh["pokemon"]
		f = open("pokemon.csv", "w")
		d = "\n".join([",".join([d['name'], str(d['num']), *(lambda x: [str(y[1]) for y in x])(d['status']), *sorted(list(d['types']))]) for d in data])
		f.write("名前, 番号, HP, こうげき, ぼうぎょ, とくこう, とくぼう, すばやさ, タイプ1, タイプ2\n")
		f.write(d)
		pprint.pprint(d)
		

if __name__ == "__main__":
	ml = Pokemon()
	#ml.data_collect()
