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
		print jdata.get('user', {}).get('name', 'Name Not Found')
		print jdata.get('text')
 
		retweeted = jdata.get('retweeted', None)
		from_self = jdata.get('user',{}).get('id_str','') == "3068055436"
		people = jdata.get('entities', {}).get('user_mentions', [])
		peoplenames = getUniques([i.get('screen_name') for i in people])
		while name in peoplenames:
			peoplenames.remove(name)
		peoplenames.insert(0, name)
		if "postingshittily" in peoplenames:
			peoplenames.remove("postingshittily")
		names = " ".join(["@{}".format(i) for i in peoplenames if i])
 
		if jdata.get('text')[:2] != "RT" and not retweeted and not from_self:
			try:
				text = generate(debug=True)
				api.update_status(status=names+" "+text, in_reply_to_status_id = jdata.get('id_str', ''))
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
	while True:
		stream.filter(track=[config["searchfor"]])

def cleanup():
	global replyThread, mainThread
	replyThread.terminate()
	mainThread.terminate()

def centralmain():
	global replyThread, mainThread
	atexit.register(cleanup)
	if not os.path.exists(os.path.join(path, "shitpostconfig.json")):
		file = open(os.path.join(path, "shitpostconfig.json"), "w")
		file.write("{\"time\": 360,\"notifytime\": 60,\"searchfor\": \"gimme a shitpost\"}")
		file.close()
	replyThread = multiprocessing.Process(target=tweetStream)
	mainThread = multiprocessing.Process(target=main)
	replyThread.start()
	mainThread.start()
	try:
		while True: time.sleep(0.001)
	except KeyboardInterrupt: cleanup()

if __name__ == "__main__": centralmain()