# coding=utf-8
from shitpostbot import *
import atexit
import multiprocessing
path = os.path.dirname(sys.argv[0])

def getUniques(l):
	nl = l[:]
	cl = l[:]
	for i in l:
		intimes = 0
		while i in cl:
			intimes += 1
			cl.remove(i)
		if intimes > 1:
			for j in xrange(intimes-1):
				nl.remove(i)
	return nl


class cSL(tweepy.StreamListener):
 
	def on_data(self, data):
		jdata = json.loads(data.strip())
		name = jdata.get('user', {}).get('screen_name', 'Name Not Found')
		selfname = api.me().screen_name
		print jdata.get('user', {}).get('name', 'Name Not Found')
		print jdata.get('text')
 
		retweeted = jdata.get('retweeted', None)
		from_self = jdata.get('user', {}).get('id',0) == api.me().id
		people = jdata.get('entities', {}).get('user_mentions', [])
		peoplenames = getUniques([i.get('screen_name') for i in people])
		if name in peoplenames:     peoplenames.remove(name)
		if selfname in peoplenames: peoplenames.remove(selfname)
		peoplenames.insert(0, name)
		names = " ".join(["@{}".format(i) for i in peoplenames if i])

		dot = "." if "public" in jdata.get('text', '') else ""

		if jdata.get('text', '')[:2] != "RT" and not retweeted and not from_self:
			try:
				text = generate(debug=True)
				api.update_status(status=dot+names+" "+text, in_reply_to_status_id = jdata.get('id_str', ''))
			except Exception, e:
				print "failed: "+str(e)
		time.sleep(2)

		return True
 
	def on_error(self, status):
		print status
		time.sleep(5)
		return True
 
def tweetStream():
	config = json.load(open(os.path.join(path, "shitpostconfig.json")))
	l = cSL()
	stream = tweepy.Stream(api.auth, l)

	targets = []
	if isinstance(config.get("searchfor"), str):
		targets.append(config.get("searchfor"))
	elif isinstance(config.get("searchfor"), list):
		targets = config.get("searchfor")
	else:
		targets = ["gimme a shitpost", "gimme a public shitpost"]

	while True:
		try:
			stream.filter(track=targets)
		except Exception, e:
			if type(e) is KeyboardInterrupt: break
			print "failed: "+str(e)

def cleanup():
	global replyThread, mainThread
	replyThread.terminate()
	mainThread.terminate()

def centralmain():
	global replyThread, mainThread
	atexit.register(cleanup)
	if not os.path.exists(os.path.join(path, "shitpostconfig.json")):
		json.dump({
			"time": 360,
			"notifytime": 60,
			"searchfor": ["gimme a shitpost", "gimme a public shitpost"]
			}, open(os.path.join(path, "shitpostconfig.json"), "w"), indent=2, sort_keys=True)
	replyThread = multiprocessing.Process(target=tweetStream)
	mainThread = multiprocessing.Process(target=main)
	replyThread.start()
	mainThread.start()
	try:
		while True: time.sleep(0.001)
	except KeyboardInterrupt: cleanup()

if __name__ == "__main__": centralmain()