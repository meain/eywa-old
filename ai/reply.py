from aimlbot import *
import wolframapi as wapi
import imageapi as iapi

def get_result(query, user_id, k):
	'''
	This fucniton diverts the querry to different routes
	'''
	if query == "hey":
		return "Hey " + user_id
	if query.split(' ', 1)[0] == 'wolfram':
		query = query.split(' ', 1)[1]
		print "Wolfram query : " + query
		wresult,wdat = wapi.frame_and_request(query)
		return wdat
	if query.split(' ', 1)[0] == 'image':
		query = query.split(' ', 1)[1]
		print "Image query : " + query
		wsuccess, wlink = iapi.get_image(query)
		if wsuccess == True:
			return wlink
		else:
			return 'No image'		#Hope it will never be used
	else:
		# the aiml takes time to load, will have to run it in a parallel thread
		return reply_aiml(query, k)
'''
get the user id then we can use it from the python insterface so as to get the information from the google server by querrying with the id
a possible problem is that our python app wont be able queey directly -
	-- either register python app and chang the whole login thing into python
	-- or pipe python querry through the html server ;)
'''
