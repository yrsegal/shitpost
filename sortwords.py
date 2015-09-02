import json, os, time, re

whitespace = re.compile(r"\s+")

path = os.path.dirname(__file__)
wordpath = os.path.join(path, "words.json")
if __name__ == "__main__":
	words = json.load(open(wordpath))
	nwords = {}
	for i in words:
		if not isinstance(words[i], list): continue
		nwordsi = []
		for j in words[i]:
			if j not in nwordsi:
				j = whitespace.sub(" ", j.replace(".", "").lower().strip().rstrip())
				nwordsi.append(j)
		nwordsi.sort()
		nwords[i] = nwordsi
	nwords["_timestamp"] = "Generated at "+time.asctime(time.gmtime()) + " UTC"
	json.dump(nwords, open(wordpath, "w"), indent=2, sort_keys=True)