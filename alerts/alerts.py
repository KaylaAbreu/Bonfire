import requests


class Alerts():
    def __init__(self):
        # Initialize headlines for dialog box in Welcome Screens
        self.headline1 = None
        self.headline2 = None
        self.headline3 = None

    def alerts(self):
        state = "NC"
        response = requests.get(f'https://api.weather.gov/alerts/active?area={state}').json()

        mountains = ['Cherokee;', 'Graham;', 'Clay;', 'Macon;', 'Swain;', 'Jackson;', 'Haywood;', 'Transylvania;',
                     'Henderson;', 'Buncombe;', 'Madison;', 'Yancey;', 'Mitchell;', 'McDowell;', 'Rutherford;', 'Polk;',
                     'Burke;', 'Caldwell;', 'Avery;', 'Watauga;', 'Ashe;', 'Wilkes;', 'Alleghany;']
        piedmont = ['Cleveland;', 'Gaston;', 'Lincoln;', 'Catawba;', 'Alexander;', 'Iredell;', 'Mecklenburg;', 'Union;',
                    'Anson;', 'Richmond;', 'Montgomery;', 'Stanly;', 'Cabarrus;', 'Rowan;', 'Moore;', 'Lee;', 'Chatham;',
                    'Randolph;', 'Davidson;', 'Davie;', 'Yadkin;', 'Forsyth;', 'Guilford;', 'Orange;', 'Wake;', 'Franklin;',
                    'Durham;', 'Orange;', 'Alamance;', 'Surry;', 'Stokes;', 'Rockingham;', 'Caswell;', 'Person;', 'Granville;',
                    'Vance;', 'Warren;']
        coast = ['Brunswick;', 'Columbus;', 'Robeson;', 'Scotland;', 'Hoke;', 'Bladen;', 'Cumberland;', 'Harnett;', 'Sampson;',
                 'Pender;', 'Duplin;', 'Onslow;', 'Jones;', 'Carteret;', 'Craven;', 'Lenior;', 'Wayne;', 'Johnston;', 'Wilson;',
                 'Nash;', 'Edgecombe;', 'Pitt;', 'Greene;', 'Pamlico;', 'Hyde;', 'Beaufort;', 'Dare;', 'Tyrrell;', 'Washington;',
                 'Martin;', 'Bertie;', 'Halifax;', 'Northampton;', 'Hertford;', 'Gates;', 'Currituck;', 'Camden;', 'Pasquotank;',
                 'Perquimans;', 'Chowan;']

        alert = False
        # Loop through mountains array and check to see if a mountain county is found in the 'areaDesc' of the JSON file
        for county in mountains:
            for i in response['features']:
                area_desc = i['properties']['areaDesc']
                if county in area_desc:
                    alert = True
                    # self.headline1 = i['properties']['headline']  # brief warning
                    # print(i['properties']['areaDesc'])          # county names
                    self.headline1 = i['properties']['description']      # What Where When Impact descriptions
                    break
                else:
                    alert = False

        if not alert:
            self.headline1 = "No Alerts at this Time"

        # Loop through piedmont array and check to see if a piedmont county is found in the 'areaDesc' of the JSON file
        for county in piedmont:
            for i in response['features']:
                area_desc = i['properties']['areaDesc']
                if county in area_desc:
                    alert = True
                    # self.headline2 = i['properties']['headline']  # brief warning
                    # print(i['properties']['areaDesc'])          # county names
                    self.headline2 = i['properties']['description']     # What Where When Impact descriptions
                    break
        if not alert:
            self.headline2 = "No Alerts at this Time"

        # Loop through coast array and check to see if a coastal county is found in the 'areaDesc' of the JSON file
        for county in coast:
            for i in response['features']:
                area_desc = i['properties']['areaDesc']
                if county in area_desc:
                    alert = True
                    # self.headline3 = i['properties']['headline']   # brief warning
                    # print(i['properties']['areaDesc'])             # county names
                    # print(i['properties']['description'])
                    self.headline3 = i['properties']['description']  # What Where When Impact descriptions
                    break

        if not alert:
            self.headline3 = "No Alerts at this Time"