import urllib, json, requests
from tqdm import tqdm
from bs4 import BeautifulSoup
 
def getLink(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    urls = []
    
    for link in soup.find_all('a'):
        urls.append(link.get('href'))

    matching = [s for s in urls if ".json" in s]
    downloadJSON(matching[0])

def downloadJSON(script_json):
    filename = script_json.split("/")[len(script_json.split("/")) - 1]
    response = requests.get(script_json, stream=True)

    with open("JSON/" + filename, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    
if __name__ == "__main__":
    url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
    getLink(url)