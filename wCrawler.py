import requests
import pandas as pd
import json

class wCrawler:
    def __init__(self):
        self.url = "https://wedy.com/graphql"
        self.payload = "{\"operationName\":null,\"variables\":{},\"query\":\"{\\n  cards(page: _PAGE_) {\\n    uid\\n    created_at\\n    content\\n    couple_name\\n    couple_image\\n    countdown\\n    wedding_slug\\n    likes_count\\n    comments_count\\n    comments_user_count\\n    __typename\\n  }\\n}\\n\"}"
        self.headers = {
            'X-User-Anonymous': "true",
            'accept': "*/*",
            'Referer': "https://app.wedy.com/",
            'Origin': "https://app.wedy.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
            'DNT': "1",
            'content-type': "application/json",
            'Cache-Control': "no-cache",
            'Host': "wedy.com",
            'accept-encoding': "gzip, deflate",
            'content-length': "263",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

    def crawlToFile(self, numberOfRequests, outputPath):
        
        cards = json.loads('{"cards": []}')
        for x in range(numberOfRequests):
            if (x%10 == 0):
                print(str(x/numberOfRequests * 100) + "% of the requests done.")  

            try:
                response = requests.request("POST", 
                    self.url,
                    data = self.payload.replace('_PAGE_', str(x)),
                    headers= self.headers
                ).json()            
                cards = {"cards": cards['cards'] + response['data']['cards']}

            except:
                # Sometimes the host may shut us down
                # Theres no point trying further in those cases
                print("Request execution aborted by an error")
                break

        print(str(numberOfRequests) + " requests done.")  

        contents = []
        for element in cards['cards']:

            id = str(element['wedding_slug'])
            
            # Inner quotes break python's json parsing, so we replace them for -
            text = str(json.loads(element['content'])['description']).replace('"', '-')
            jsonStr = r""'{ "id": "' + id + '", "text": "' + text + '" }'     

            try:                                
                card = json.loads(jsonStr, strict=False)
            except:
                # Comments might have invalid json contents, such as \o/
                # Better be safe and ignore those specific cases
                print("The following string is an invalid json that could not be parsed and was therefore ignored: " + jsonStr)
                continue                
            
            contents.append(card)

        cardsText = json.dumps(contents)    
        pd.read_json(cardsText).to_csv(outputPath)