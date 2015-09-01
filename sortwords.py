import json, os

path = os.path.dirname(__file__)
wordpath = os.path.join(path, "defaultwords.json")
if __name__ == "__main__":
	words = json.load(open(wordpath))
	for i in words:
		nwordsi = []
		for j in words[i]:
			if j not in nwordsi:
				nwordsi.append(j)
		nwordsi.sort()
		words[i] = nwordsi
	json.dump(words, open(wordpath, "w"), indent=2, sort_keys=True)