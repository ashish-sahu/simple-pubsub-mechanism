import threading
import redis

class Listener(threading.Thread):
	def __init__(self,r, channels):
		threading.Thread.__init__(self)
		self.redis = r
		self.pubsub = self.redis.pubsub()
		self.pubsub.subscribe(channels)

	def info(self, item):
 		print('{}:{}'.format(item['channel'], item['data']))
	
	def run(self):
		for item in self.pubsub.listen():
			if item['data'] == 'KILL':
				self.pubsub.unsubscribe()
				print(self, "unsubscribed and finished")
				break
			else:
				self.info(item)




if __name__ == "__main__":
	r = redis.Redis(host='localhost', port=6379, db=0)
	client = Listener(r,['pass'])
	client.start()



	r.publish('pass', 'this will reach the listener')
	r.publish('fail', 'this will not')
	r.publish('pass', 'KILL')
