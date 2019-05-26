class Country:
    def __init__(self):
        self.name
        self.code_api_data
        self.TopThingsToDO
        self.capital
        self.population = getData('population')

    def getData(self,char):
        url = 'http://inqstatsapi.inqubu.com?api_key=c5b5c1dd6b0f4ea5&countries='+ str(code)+'&data=' +str(char)+'&years=1990:2016'
        self.characteristics[char] = requests.get(url).json()
