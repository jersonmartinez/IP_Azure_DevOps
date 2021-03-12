import urllib, requests, json, os
from tqdm import tqdm
from bs4 import BeautifulSoup

class IPsAzureDevOps:
    def __init__(self, url, save_folder, property, filename):
        self.url         = url
        self.save_folder = save_folder
        self.property    = property
        self.filename    = filename

    def getData(self):
        soup = BeautifulSoup(requests.get(self.url).text, 'html.parser')
        urls = []
        
        for link in soup.find_all('a'):
            urls.append(link.get('href'))

        matching = [s for s in urls if ".json" in s]

        if not self.filename:
            self.filename = matching[0].split("/")[len(matching[0].split("/")) - 1]
        
        if not os.path.isdir(self.save_folder):
            os.system("mkdir " + self.save_folder)
        
        path = self.save_folder + "/" + self.filename
        
        try:
            open(path)
        except IOError:
            self.downloadJSON(matching[0], path)

        self.ParseJSON(path)

    def downloadJSON(self, script_json, path):
        response = requests.get(script_json, stream=True)

        with open(path, "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)

    def ParseJSON(self, path):
        json_array = json.load(open(path))
        IPs = []

        for i in range(len(json_array['values'])):
            if json_array['values'][i]['name'] == self.property: 
                IPs = json_array['values'][i]['properties']['addressPrefixes']
                break
        
        print("\nIP addresses for the property: << " + self.property + " >>\n")
        print(IPs)

if __name__ == "__main__":
    IPsAzureDevOps(
        'https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519', 
        'JSON', 
        'AzureDevOps.WestEurope',
        '' #Filename JSON
    ).getData()