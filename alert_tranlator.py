from deep_translator import GoogleTranslator
import feedparser
import requests
import argparse 
import sys
import json


posts = []

xml_file = 'todaysfeed.xml' # create file to write feed info to


def get_articles(url):
  '''
  GET request to Google Alert feed URL provided as argument
  '''
    req = requests.get(url)
    
    with open(xml_file, 'wb') as f:
        f.write(req.content)
    

def parse_print_articles(url):
  '''
  Parse XML feed to translate titles and print accompanying URL
  '''
    req = get_articles(url)
   
    with open(xml_file, 'r')as f:
        data = f.read()

    feed = feedparser.parse(data)

    for each in feed['entries']:
        posts.append({
            'title': GoogleTranslator(source='auto', target='en').translate(each['title']),
            'link': each['link'].replace('https://www.google.com/url?rct=j&sa=t&url=', '')
        })

    data = json.dumps(posts, indent=2)
    print(data)



def main():

    parser = argparse.ArgumentParser(description='Translate Google Alert Article titles and print URL'\s')
    parser.add_argument('-url', '--url', help='Google Alert RSS Feed URL')
  

    args = parser.parse_args()

                                     
    if args.url:
        
        parse_print_articles(args.url)
   
    else:
                                     
        sys.exit(1)


if __name__ == '__main__':
    main()
