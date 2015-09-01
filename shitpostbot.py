# coding=utf-8
from __future__ import print_function
from copy import deepcopy
from util import *
cprintconf.name="Shitposting"
cprintconf.color=bcolors.BROWN
config = Config(CONFIGDIR)
import random
import tweepy
import time
import json
import os
import sys

path = os.path.dirname(__file__)

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
"vampire", "video game", "walnut", "zombie", "piano", "ladder", "nostril", "illuminati", 
"selfie", "poop", "slave", "eyebrows"]

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
"wife", "wizard", "woman", "illuminati", "%n-flavored %n", "extremely %j %n"]
plurnoun = [ "%s in a %n suit", "%n fans",
"aliens from the %n planet", "anime", "asses", "babies", "beefs", "%n laws",
"bronies", "children", "dollars", "elders", "families",
"feet", "feelings", "fish", "firemen", "flamingoes", "foods", "puns", "furries", "laws",
"genitals", "knives", "milks", "members of the %ving club", "men", "money",
"pants", "%n regulations", "pastas", "pizza", "people who %v %s", "pornos",
"sheep", "spaghetties", "spies", "strawberries", "taxes",
"tragedies", "trash", "white people", "women", "words",
"aliens", "animals", "ants", "apples", "assholes", "balls", "bands",
"bears", "bees", "birds", "boobs", "books", "breasts", "boats", "boys",
"bros", "cars", "cats", "centaurs", "clowns", "communists", "cops", "corpses",
"crabs", "crimes", "dads", "desks", "dicks", "dogs", "dinosaurs",
"disgraces", "doctors", "dongs", "doors", "dragons", "ducks", "dudes",
"eels", "eggs", "failures", "fathers", "fires", "flags", "flowers", "friends",
"frogs", "games", "gamers", "genders", "giraffes", "girls", "goats",
"gods", "humans", "hotdogs", "horses", "ideas", "iguanas", "lawyers", "lemons",
"lesbians", "lizards", "lobsters", "losers", "mangos", "memes", "mimes",
"mistakes", "moms", "movies", "nerds", "orbs", "original characters",
"plants", "pets", "pirates", "rabbits", "racoons", "rats", "regrets", "republicans",
"robots", "sharks", "shovels", "skeletons", "sins", "sons", "snakes",
"spiders", "spoons", "sports", "sticks", "teenagers", "trees", "trains", "traitors",
"vampires", "video games", "walnuts", "zombies", "marmite", "salad", "penises", "pikmin", "international %n treaties",
"%a kinky %s", "poops"]

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
"weaponized", "fatherly", "dank", "arousing", "funny" ]
plusadj = [ "concerningly", "desperately", "disgustingly", "impossibly",
"incredibly", "mostly", "obviously", "only", "otherwise", "really",
"secretly", "slightly", "suprisingly", "unfortunately", "very",
"wildly", "arousingly", "forcefully", "furiously" ]
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
"your %s %ved my %n", "get away from my %n", "how can %s be real if %s aren't real", 
"help, my %n won't stop %ving", "am I a %n", "%s should really %v %s", "%s??? %s!", "eat all the %s", 
"I sexually identify as a %j %n.", "%ving is as easy as %ving %s", "if %s came from %s, then why are there still %s?",
"i like to %v my %n %a", "*%a %vs*"]
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
		if debug: cprint(base)
		base = base.replace("%s", randpop(temps), 1)
		base = base.replace("%j", randpop(tempj), 1)
		base = base.replace("%n", randpop(tempn), 1)
		base = base.replace("%a", randpop(tempav), 1)
		while "%ved" in base:
			base = base.replace("%ved", randpop(tempve), 1)
		base = base.replace("%v", randpop(tempv), 1)
		base = base.replace("%i", str(random.randint(2, 20)), 1)
	if debug: cprint(base)
	if "override" in config:
		tempconf = config.data
		cprint("Overriding generated text.", color=bcolors.YELLOW)
		base = config["override"]
		cprint(format("New text: {endc}{base}", base=base), color=bcolors.YELLOW)
		del tempconf["override"]
		json.dump(tempconf, open(os.path.join(path, "shitpostconfig.json"), "w"), indent = 2)
	return base

authKeyPath = os.path.dirname(sys.argv[0])
if not os.path.exists(os.path.join(authKeyPath, "authkeys.json")):
	json.dumps({
		"TWITTER_CONSUMER_KEY": "",
		"TWITTER_CONSUMER_SECRET": "",
		"TWITTER_ACCESS_KEY": "",
		"TWITTER_ACCESS_SECRET": ""
		}, open(os.path.join(authKeyPath, "authkeys.json"), "w"), indent=2, sort_keys=True)

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
	try:
		from netifaces import interfaces, ifaddresses, AF_INET
	except: return ["install netifaces >:("]
	ips = []
	for ifaceName in interfaces():
		addresses = [i['addr'] for i in ifaddresses(ifaceName).get(AF_INET, [{"addr":"not found"}])]
		if "not found" not in addresses and "127.0.0.1" not in addresses:
			ips += addresses
	if not ips and not test: 
		ips.append("localhost")
	return ips

def main():
	while True:
		try:
			text = generate(debug=True)
			
			while not connected_to_internet():
				time.sleep(1)
			try:
				api.update_status(status=text)
				cprint(format("Made tweet: {text}", text=text))
			except Exception, e:
				if isinstance(e, KeyboardInterrupt):
					break
				cprint(tbformat(e, "Error sending tweet:"), color=bcolors.YELLOW)
			started = time.time()
			stopped = time.time()
			cprint("Slept 0 seconds.")
			while stopped-started < config.get("time", 360):
				if not int(stopped-started) % config.get("notifytime", 60) and int(stopped-started) != 0: 
					print(bcolors.REMAKELINE, end="")
					cprint("Slept "+str(int(stopped-started))+" seconds.")
				time.sleep(1)
				stopped = time.time()

			if int(stopped-started) != config.get("notifytime", 60): print(bcolors.REMAKELINE, end="")
			cprint("Slept "+str(config["time"])+" seconds.")
		except KeyboardInterrupt:
			pass


if __name__ == "__main__": main()
