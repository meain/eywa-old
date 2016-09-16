'''
Uses google customsearch api to obtain images
'''
from apiclient.discovery import build

def get_image(query):
    # Create api object
    service = build("customsearch", "v1",
               developerKey="AIzaSyCx1ojOp7vEmfuX3FxvRjx4_EZGGMCvyX8")

    # Excecute query
    res = service.cse().list(
        q=query,
        cx='001255247134752793628:fqtqc5hatm4',
        searchType='image',
        num=3,
        safe= 'off'
    ).execute()

    # Return result
    if not 'items' in res:
        return False,""
    else:
        #Currently returning only the link to first image
        print res['items'][0]['link']
        return True, res['items'][0]['link']
