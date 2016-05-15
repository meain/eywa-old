from apiclient.discovery import build

def get_image(query):
    service = build("customsearch", "v1",
               developerKey="AIzaSyCx1ojOp7vEmfuX3FxvRjx4_EZGGMCvyX8")

    res = service.cse().list(
        q=query,
        cx='001255247134752793628:fqtqc5hatm4',
        searchType='image',
        num=3,
        # imgType='clipart',
        # fileType='png',
        safe= 'off'
    ).execute()

    #print res

    if not 'items' in res:
        #print 'No result !!\nres is: {}'.format(res)
        return False,""
    else:
        '''
        for item in res['items']:
            #print('{}:\n\t{}'.format(item['title'], item['link']))
            print item['title'] + "\n\t" + item['link']
        '''
        #Currently returning only the link to one image
        print res['items'][0]['link']
        return True, res['items'][0]['link']


#print get_image('baby')
