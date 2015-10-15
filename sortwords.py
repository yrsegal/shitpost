import json, os, time, re, string

whitespace = re.compile(r"\s+")

path = os.path.dirname(__file__)
wordpath = os.path.join(path, "words.json")
if __name__ == "__main__":
	words = json.load(open(wordpath))
	for i in words:
		if isinstance(words[i], list): 
			nwords = []
			for j in words[i]:
				if j not in nwords:
					j = whitespace.sub(" ", j.replace(".", "").lower().strip().rstrip())
					nwords.append(j)
			nwords.sort()
			words[i] = nwords
	words["#timestamp"] = "Generated at "+time.asctime(time.gmtime()) + " UTC"
	wordtext = ''.join(filter(lambda x: x in string.printable, json.dumps(words, indent=2, sort_keys=True)))
	open(wordpath, "w").write(wordtext)