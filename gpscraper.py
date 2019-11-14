from PIL import Image, ImageFile
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from slugify import slugify
from io import BytesIO

ImageFile.LOAD_TRUNCATED_IMAGES = TrueFILE_WITH_LINKS = 'test.txt'

def get_image(line):
    for retry in range(1,11):
        try:
            r = requests.get(line, timeout=(10,10))
            #print(r.text)
            bs = BeautifulSoup(r.text, features="html.parser")
            link = bs.find('img')['src']
            title = bs.find('meta', property='og:title')['content']
            line_split = line.split('/')
            date_str = line_split[4]+"-"+line_split[5].zfill(2)+"-"+line_split[6].zfill(2)
            my_file = Path("comics/"+date_str+"_"+slugify(title)+".png")
            if my_file.is_file():
                print("ALREADY EXISTS: "+date_str+" "+link+" "+title)
               
            r2 = requests.get(link, timeout=(10,10))
            i = Image.open(BytesIO(r2.content))
            i.save("comics/"+date_str+"_"+slugify(title)+".png", "PNG")
            print("OK: "+date_str+" "+link+" "+title)
            return
        except Exception:
            if r.status_code != 200:
                print("WAIT1 ("+str(retry)+"/10): "+str(r.status_code)+" "+ line)
                continue
            else:
                if r2.status_code != 200:
                    print("WAIT2 ("+str(retry)+"/10): "+str(r2.status_code)+" "+ line)
                    continue
                else:
                    print(r.text)
                    print(traceback.format_exc())
                    return
    print("FATAL ERROR: "+line)
   
def scrape_images():
    pool = Pool(4)
    lines = [line.rstrip('\n') for line in open(FILE_WITH_LINKS)]
    pool.map(get_image, lines)
   
if __name__ == '__main__':
    scrape_images()