##simple testing routines
class rngd_test:
	_t_counter = 0
	_failed = 0

	def _assert(msg, expr):
		rngd_test._t_counter += 1
		if expr:
			print('rngd_test: [{}] passed'.format(msg))
		else:
			print('rngd_test: [{}] failed!'.format(msg))
			rngd_test._failed += 1
	def _finish():
		print('rngd_test: {}/{} tests failed'.format(rngd_test._failed, rngd_test._t_counter))


from rngd import *

##nanokv tests
testdb = rngd_nanokv()

testdb.execute('store test test1')
rngd_test._assert('nanokv store/get', testdb.execute('get test')=='test1')
rngd_test._assert('nanokv search', testdb.execute('search test'))
##geeration tests

state = 'testtest'

new_state, bytes = rngd_generate(state)

rngd_test._assert('rngd_generate state change', new_state != state)
rngd_test._assert('rngd_generate output length', len(bytes)==256*2)

rngd_test._finish()
