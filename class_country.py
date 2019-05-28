def update_output_div(country):
    if attractions[country][0:6] != []:
        no_data =''
    else:
        no_data = 'No DATA AVAILABLE :('
    return 'TOP places to visit in {}: {}'.format(country, no_data)

class Country:
    def __init__(self):
        self.name
        self.code_api_data
        self.TopThingsToDO = top_things_to_do()
        self.capital = getData('capital_name')
        self.population = getData('population')

    def getData(self,charcteristics):
        url = 'http://inqstatsapi.inqubu.com?api_key=c5b5c1dd6b0f4ea5&countries='+countries.get(self)+'&data=' +charcteristics+'&years=1990:2016'
        return requests.get(url).json()


    def top_things_to_do(self):
        with open('Tripadvisor.json', 'r') as f:
                datastore = json.load(f)
        datastore
        attractions = {}
        for country in datastore:
            attractions[country['country']]=country['attractions']
        if attractions[country][0:6] != []:
            return attractions[country][0], attractions[country][1], attractions[country][2],attractions[country][3], attractions[country][4]
        else:
            return 'NA','NA','NA','NA','NA'
