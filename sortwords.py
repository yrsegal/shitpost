import json, os, time

path = os.path.dirname(__file__)
wordpath = os.path.join(path, "defaultwords.json")
if __name__ == "__main__":
	words = json.load(open(wordpath))
	nwords = {}
	for i in words:
		if not isinstance(words[i], list): continue
		nwordsi = []
		for j in words[i]:
			if j not in nwordsi:
				j = j.replace(".", "")
				j = j.lower()
				nwordsi.append(j)
		nwordsi.sort()
		nwords[i] = nwordsi
	nwords["_timestamp"] = "Generated at "+time.asctime()
	json.dump(words, open(wordpath, "w"), indent=2, sort_keys=True)