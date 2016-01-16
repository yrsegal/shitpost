# coding=utf-8
from __future__ import print_function
from wireutils import *
color_printing_config.name="Shitposting"
color_printing_config.color=ansi_colors.BROWN
import random
import tweepy

path = os.path.dirname(__file__)
CONFIGDIR = os.path.join(path, "shitpostconfig.json")
if not os.path.exists(CONFIGDIR):
	json.dump({
		"time": 360,
		"notifytime": 60,
		"searchfor": ["gimme a shitpost", "gimme a public shitpost"],
		"public": "public",
		"notags": ["just", "do it"]
		}, open(os.path.join(path, "shitpostconfig.json"), "w"), indent=2, sort_keys=True)
config = Config(CONFIGDIR)
	


genobjects = Config(os.path.join(path, "words.json"))
def randsub(string, regex):
	global genwords
	if regex not in genwords or not genwords[regex]:
		genwords[regex] = genobjects[genobjects["@replaces"][regex]][:]
	word = genwords[regex].pop(random.randrange(len(genwords[regex])))
	return re.sub("%"+regex, word, string, 1)

if not os.path.exists(os.path.join(path, "words.json")):
	raise ValueError("There aren't any words to generate from!")


genwords, bases = {}, []
def generate(debug=False):
	global genwords, bases

	if not bases:
		bases = genobjects["@bases"]
	base = bases.pop(random.randrange(len(bases)))

	while "%" in base:
		if debug: color_print(base)
		for regex in genobjects["@replaces"]:
			base = randsub(base, regex)
		
	if debug: color_print(base)
	if "override" in config:
		tempconf = config.data
		color_print("Overriding generated text.", color=ansi_colors.YELLOW)
		base = config["override"]
		color_print(format("New text: {endc}{base}", base=base), color=ansi_colors.YELLOW)
		del tempconf["override"]
		json.dump(tempconf, open(os.path.join(path, "shitpostconfig.json"), "w"), indent = 2)
	genobjects.reload()
	return base

authKeyPath = os.path.dirname(sys.argv[0])
if not os.path.exists(os.path.join(authKeyPath, "authkeys.json")):
	json.dump({
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
				color_print(format("Made tweet: {text}", text=text))
			except Exception, e:
				if isinstance(e, KeyboardInterrupt):
					break
				color_print(format_traceback(e, "Error sending tweet:"), color=ansi_colors.YELLOW)
			started = time.time()
			stopped = time.time()
			color_print("Slept 0 seconds.")
			while stopped-started < config.get("time", 360):
				if not int(stopped-started) % config.get("notifytime", 60) and int(stopped-started) != 0: 
					print(ansi_colors.REMAKELINE, end="")
					color_print("Slept "+str(int(stopped-started))+" seconds.")
				time.sleep(1)
				stopped = time.time()

			if int(stopped-started) != config.get("notifytime", 60): print(ansi_colors.REMAKELINE, end="")
			color_print("Slept "+str(config["time"])+" seconds.")
		except KeyboardInterrupt:
			pass


if __name__ == "__main__": main()
