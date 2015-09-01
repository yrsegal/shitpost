import json, os

path = os.path.dirname(__file__)
wordpath = os.path.join(path, "defaultwords.json")
if __name__ == "__main__":
	words = json.load(open(wordpath))
	for i in words:
		words[i].sort()
	json.dump(words, open(wordpath, "w"), indent=2, sort_keys=True)