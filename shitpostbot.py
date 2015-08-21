# coding=utf-8

from copy import deepcopy
import random
import tweepy
import time
import json
import os
import sys

basenoun = [ "%n-worshipping cult", "%n %ver",
"alien", "animal", "ant", "apple", "asshole", "ball", "band",
"bear", "bee", "bird", "boob", "book", "breast", "boat", "boy",
"bro", "car", "cat", "centaur", "clown", "communist", "cop", "corpse",
"crab", "crime", "dad", "desk", "dick", "dog", "dinosaur",
"disgrace", "doctor", "dong", "door", "dragon", "duck", "dude",
"eel", "egg", "failure", "father", "fire", "flag", "flower", "friend",
"frog", "game", "gamer", "gender", "giraffe", "girl", "goat",
"god", "human", "hotdog", "horse", "idea", "iguana", "lawyer", "lemon",
"lesbian", "lizard", "lobster", "loser", "mango", "meme", "mime",
"mistake", "mom", "movie", "nerd", "orb", "original character",
"plant", "pet", "pirate", "rabbit", "racoon", "rat", "regret", "republican",
"robot", "shark", "shovel", "skeleton", "sin", "son", "snake",
"spider", "spoon", "sport", "stick", "teenager", "tree", "train", "traitor",
"vampire", "video game", "walnut", "zombie" ]

singnoun = [ "%n with %i %s", "agenda", "ass",
"baby", "blender", "bowl of soup", "brony", "%n mixed with a %n",
"cactus", "child", "disaster", "dissapointment",
"%n shaped like a %n", "family", "feel", "fish", "flamingo", "fox",
"fruit", "furry", "grandma", "godess", "group of %s", "husband",
"life", "mailman", "man", "%n with a fetish for %s", "mustache",
"%n with the head of a %n", "movie trilogy", "number of %s",
"piece of shit", "pizza", "princess", "rhino", "sign from god",
"country of %s", "snowman", "strongly-worded letter",
"%n with a %n allergy", "sum of money", "spy", "taste of humanity",
"%n and their army of %s", "taxidermy", "tragedy", "werewolf",
"wife", "wizard", "woman" ]
plurnoun = [ "%s in a %n suit", "%n fans",
"aliens from the %n planet", "anime", "asses", "babies", "beefs", "%n laws",
"bronies", "children", "dollars", "elders", "families",
"feet", "feelings", "fish", "firemen", "flamingoes", "foods", "puns", "furries", "laws",
"genitals", "knives", "milks", "members of the %ving club", "men", "money",
"pants", "%n regulations", "pastas", "pizza", "people who %v %s", "pornos",
"sheep", "spaghetties", "spies", "strawberries", "taxes",
"tragedies", "trash", "white people", "women", "words" ]
adjective = [ "%n-shaped", "%n-hating", "%n-%ving", "american",
"angry", "animated", "annoying", "awful", "bad", "beautiful",
"big", "boring", "burning", "capitalist", "cheating", "cis",
"bisexual", "cisgender", "confused", "confusing", "communist",
"controversial", "crusty", "cute", "dead", "deadly", "delicious",
"disgraceful", "disguised", "disgruntled", "digusting",
"disrespectful", "dissapointing", "desperate", "evil", "feminist",
"fucked up", "fucking", "gay", "girl", "handsome", "heterosexual", "homosexual", "hot",
"hungry", "illegal", "juicy", "large", "lesbian", "liberal",
"immortal", "innocent", "kinky", "moist", "miserable", "missing",
"naked", "nasty", "naughty", "old", "overrated", "pet", "pissed off", "popular",
"possessed", "precious", "pretentious", "poisonous", "popular",
"republican", "screaming", "sentient", "sexist", "sexy", "shitty", "simple",
"slimey", "small", "smelly", "stoned", "space", "strong",
"suburban", "tasty", "tender", "tiny", "trans", "transgender",
"transphobic", "unacceptable", "undead", "unexpected",
"unstoppable", "unused", "unwanted", "useless", "weak",
"weaponized", "fatherly" ]
plusadj = [ "concerningly", "desperately", "disgustingly", "impossibly",
"incredibly", "mostly", "obviously", "only", "otherwise", "really",
"secretly", "slightly", "suprisingly", "unfortunately", "very",
"wildly" ]
prefix = [ "%s", "%s?", "%j %n", "%i %s",
"%a %v your %n", "%s are %j", "%s aren’t that %j",
"%s are %j but can they %v this *%vs a %n*", "a %n that isn’t %j",
"*%vs a %n* you %j %n", "%i reasons why %s are %j",
"%v your %n with a %n", "%v a %n’s %s", "%v %s", "%v a %n",
"%s who %v %s are %j", "%s %v %i %s", "%s must %v %a",
"%s %ved my %n", "%v your %n", "%v your own %n",
"%ved a %n so %a it %ved a %n", "%v a %n who doesn’t %v %s",
"%v a %n who won’t %v you", "%v your %s", "a %n",
"%s can’t %v %s because of %s", "%s who %v %s with their %s",
"%a attempting to %v my %s", "all %s are %s",
"are %s really just %s", "can %s %v", "can %s %v me",
"can %s %v %s", "can i %v a %n", "can %s and %s %v each other",
"do not %v a %n", "do not %v %s", "how to get a %n to %v %s",
"i %v %s not %s", "i never %ved a %n who wasn’t %j",
"i will %v a %n", "i will not let %s %v my %n", "more %s",
"try %ving a %n", "what about %s", "who needs %s when you have %s",
"would you rather %v a %n or a %n", "who put %s on my %n",
"why are %s so %j", "why aren’t %s %j", "why %v %s when you can %v a %n",
"why not %v %s", "why do %s %v me?", "why did i %v a %n",
"you can’t %v %s", "you can’t prove %s aren’t %s",
"your %s %ved my %n" ]
verb = [ "abandon", "adopt", "annoy", "attack", "arouse",
"avoid", "beat", "befriend", "build", "burn", "buy", "caress",
"confuse", "cosplay", "count", "date", "doxx", "destroy", "disrespect",
"dissapoint", "draw", "eat", "end", "enjoy", "feed", "feel",
"fight", "find", "fix", "forget", "fuck", "hate", "help", "hug",
"insult", "intimdate", "irritate", "kick", "kill", "kiss", "lick",
"love", "marry", "meet", "outrun", "overthrow", "prevent", "punch", "punish",
"regret", "remember", "resist", "respect", "ruin", "save",
"seduce", "smack", "smell", "stab", "suck", "stop", "study", "trust",
"understand", "upset", "watch", "win", "worship" ]
pastverb = [ "abandoned", "adopted", "annoyed", "attacked", "aroused",
"avoided", "beaten", "befriended", "built", "burned", "bought", "caressed",
"confused", "cosplayed", "counted", "dated", "doxxed", "destroyed", "disrespected",
"dissapointed", "drew", "ate", "ended", "enjoyed", "fed", "felt",
"fought", "found", "fixed", "forgot", "fucked", "hated", "helped", "hugged",
"insulted", "intimdated", "irritated", "kicked", "killed", "kissed", "licked",
"loved", "married", "met", "outran", "overthrew", "prevented", "punched", "punished",
"regretted", "remembered", "resisted", "respected", "ruined", "saved",
"seduced", "smacked", "smelled", "stabbed", "sucked", "stopped", "studied", "trusted",
"understood", "upset", "watched", "won", "worshipped" ]
adverb = [ "accidentally", "carefully", "casually",
"desperately", "eventually", "fondly", "gently", "immidiately",
"purposely", "quickly", "seductively", "slowly", "softly",
"sucessfully", "tenderly" ]

def randpop(iterable):
	if len(iterable) == 0:
		return random.choice(adverb)
	return iterable.pop(random.randrange(len(iterable)))


def generate(debug=False):
	temps = deepcopy(plurnoun)
	tempj = deepcopy(adjective)
	tempn = deepcopy(basenoun)+deepcopy(singnoun)
	tempav = deepcopy(adverb)
	tempve = deepcopy(pastverb)
	tempv = deepcopy(verb)
	base = random.choice(prefix)

	while "%" in base:
		if debug: print(base)
		base = base.replace("%s", randpop(temps), 1)
		base = base.replace("%j", randpop(tempj), 1)
		base = base.replace("%n", randpop(tempn), 1)
		base = base.replace("%a", randpop(tempav), 1)
		while "%ved" in base:
			base = base.replace("%ved", randpop(tempve), 1)
		base = base.replace("%v", randpop(tempv), 1)
		base = base.replace("%i", str(random.randint(2, 20)), 1)
	if debug: print(base)
	return base

authKeyPath = os.path.dirname(sys.argv[0])
if not os.path.exists(os.path.join(authKeyPath, "authkeys.json")):
	json.dumps({
		"TWITTER_CONSUMER_KEY": "",
		"TWITTER_CONSUMER_SECRET": "",
		"TWITTER_ACCESS_KEY": "",
		"TWITTER_ACCESS_SECRET": ""
		}, open(os.path.join(authKeyPath, "authkeys.json"), "w"), , indent=2, sort_keys=True)

a = json.load(open(os.path.join(authKeyPath, "authkeys.json")))

auth = tweepy.OAuthHandler(a["TWITTER_CONSUMER_KEY"], a["TWITTER_CONSUMER_SECRET"])
auth.set_access_token(a["TWITTER_ACCESS_KEY"], a["TWITTER_ACCESS_SECRET"])
api = tweepy.API(auth)	

def connected_to_internet():
	return bool(getIps(test=True))
def getIps(test=False):
	"""
	Get the IPs this device controls.
	"""
	from netifaces import interfaces, ifaddresses, AF_INET
	ips = []
	for ifaceName in interfaces():
		addresses = [i['addr'] for i in ifaddresses(ifaceName).get(AF_INET, [{"addr":"not found"}])]
		if "not found" not in addresses and "127.0.0.1" not in addresses:
			ips += addresses
	if not ips and not test: 
		ips.append("localhost")
	return ips

def main():
	path = os.path.dirname(sys.argv[0])
	if not os.path.exists(os.path.join(path, "shitpostconfig.json")):
		file = open(os.path.join(path, "shitpostconfig.json"), "w")
		file.write("{\"time\": 360,\"notifytime\": 60,\"searchfor\": \"gimme a shitpost\"}")
		file.close()
	lastmodtime = os.path.getctime(os.path.join(path, "shitpostconfig.json"))
	config = json.load(open(os.path.join(path, "shitpostconfig.json")))
	while True:
		if os.path.getctime(os.path.join(path, "shitpostconfig.json")) > lastmodtime:
			config = json.load(open(os.path.join(path, "shitpostconfig.json")))
			lastmodtime = os.path.getctime(os.path.join(path, "shitpostconfig.json"))
		text = generate(debug=True)
		if "override" in config:
			print("overriding")
			text = config["override"]
			print(text)
			del config["override"]
			json.dump(config, open(os.path.join(path, "shitpostconfig.json"), "w"), indent = 2)
		
		while not connected_to_internet():
			time.sleep(1)

		api.update_status(status=text)
		print(text)
		print("\n")
		started = time.time()
		stopped = time.time()
		while stopped-started < config.get("time", 360):
			if os.path.getctime(os.path.join(path, "shitpostconfig.json")) > lastmodtime:
				config = json.load(open(os.path.join(path, "shitpostconfig.json")))
				lastmodtime = os.path.getctime(os.path.join(path, "shitpostconfig.json"))
			if not int(stopped-started) % config.get("notifytime", 60) and int(stopped-started) != 0: 
				print("Slept "+str(int(stopped-started))+" seconds.")
			time.sleep(1)
			stopped = time.time()
		print("Slept "+str(config["time"])+" seconds.")
		print(" ")


if __name__ == "__main__": main()