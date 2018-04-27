## basic imports
import hashlib, uuid, random, string #used for prng
from flask import *

## simple in-memory db
# maps string -> string

#commands:
#nanokv.execute('store <key> <value>') -> None
#nanokv.execute('search <key>') -> Bool
#nanokv.execute('get <key>') -> String


class rngd_nanokv:
	def __init__(self):
		self._kv = dict()
	def execute(self, cmd):
		cmd = cmd.split()
		if cmd[0] == 'store':
			self._kv[cmd[1]] = cmd[2]
			return
		if cmd[0] == 'search':
			if cmd[1] in self._kv.keys():
				return True
			return False

		if cmd[0] == 'get':
			return self._kv[cmd[1]]

		

## pure function (String) -> (String, String)
# takes state as argument, outputs modified state and a 256-byte block of random numbers

def rngd_generate(state):
	_inner_block = ''
	for i in range(8):
		_inner_block += hashlib.sha256(bytes(state, 'utf-8')).hexdigest()
		state = state[:-64] + hashlib.sha256(bytes(state, 'utf-8')).hexdigest()
	return (state, _inner_block)





app = Flask(__name__)
db = rngd_nanokv()
@app.route('/', methods = ['GET'])
def default():
	return render_template('./static.html')


@app.route('/new', methods = ['POST'])
def new_instance():
	seed = ''.join(random.choices(string.ascii_lowercase + string.digits, k=64))
	token = uuid.uuid4().hex
	print('rngd: new instance with token:', token)
	db.execute('store {} {}'.format(token, seed))
	return token, 200


@app.route('/get/<token>', methods = ['GET'])
def do_gen(token):
	try:
		state = db.execute('get {}'.format(token))
		state, bytes = rngd_generate(state)
		db.execute('store {} {}'.format(token, state))
		print('rngd: responded with token:', token)
		return bytes, 200
	except KeyError as e:
		print('rngd: 404 with token:', token)
		return 'no such token', 404

@app.route('/entropy/<token>', methods = ['GET'])
def get_ent(token):
	try:
		state = db.execute('get {}'.format(token))
		print('rngd: returned entropy with token:', token)
		return state, 200
	except KeyError as e:
		print('rngd: 404 with token:', token)
		return 'no such token', 404


if __name__ == '__main__':
	app.run(port = 8080)
