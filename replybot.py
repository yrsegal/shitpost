
from shitpostbot import *
import atexit
import multiprocessing

class cSL(tweepy.StreamListener):
 
	def on_data(self, data):
		jdata = json.loads(data.strip())
		print jdata.get('text')
 
		retweeted = jdata.get('retweeted', None)
		from_self = jdata.get('user',{}).get('id_str','') == "3068055436"
 
		if jdata.get('text')[:2] != "RT" and not retweeted and not from_self:
			try:
				text = generate(debug=True)
				print(text)
				api.update_status(status="@"+jdata.get('user', {}).get('screen_name')+" "+text, in_reply_to_status_id = jdata.get('id_str', ''))
			except Exception, e:
				print "failed: "+str(e)
		time.sleep(2)

		return True
 
	def on_error(self, status):
		print status
		time.sleep(5)
		return True
 
def tweetStream():
	l = cSL()
	stream = tweepy.Stream(api.auth, l)
	while True:
		stream.filter(track=["gimme a shitpost"])

def cleanup():
	global replyThread, mainThread
	replyThread.terminate()
	mainThread.terminate()

def centralmain():
	global replyThread, mainThread
	atexit.register(cleanup)
	replyThread = multiprocessing.Process(target=tweetStream)
	mainThread = multiprocessing.Process(target=main)
	replyThread.start()
	mainThread.start()
	try:
		while True: time.sleep(0.001)
	except KeyboardInterrupt: cleanup()

if __name__ == "__main__": centralmain()