import os
import pickle
import psycopg2
import pandas as pd
import sqlalchemy
from collections import defaultdict

# parameters
languages = {
    'English (US)': {
        'name': 'English (US)',
        'lang': 'en',
        'tld': 'com'
    },
    'English (UK)': {
        'name': 'English (UK)',
        'lang': 'en',
        'tld': 'co.uk'
    },
    'English (Australia)': {
        'name': 'English (Australia)',
        'lang': 'en',
        'tld': 'com.au'
    },
    'English (Canada)': {
        'name': 'English (Canada)',
        'lang': 'en',
        'tld': 'ca'
    },
    'English (New Zealand)': {
        'name': 'English (New Zealand)',
        'lang': 'en',
        'tld': 'co.nz'
    },
    'English (Ireland)': {
        'name': 'English (Ireland)',
        'lang': 'en',
        'tld': 'ie'
    },
    'English (South Africa)': {
        'name': 'English (South Africa)',
        'lang': 'en',
        'tld': 'co.za'
    },
    'English (India)': {
        'name': 'English (India)',
        'lang': 'en',
        'tld': 'in'
    },
    'Spanish (Mexico)': {
        'name': 'Spanish (Mexico)',
        'lang': 'es',
        'tld': 'com.mx'
    },
    'Spanish (Spain)': {
        'name': 'Spanish (Spain)',
        'lang': 'es',
        'tld': 'es'
    },
    'Portuguese (Brazil)': {
        'name': 'Portuguese (Brazil)',
        'lang': 'pt',
        'tld': 'com.br'
    },
    'Portuguese (Portugal)': {
        'name': 'Portuguese (Portugal)',
        'lang': 'pt',
        'tld': 'pt'
    },
    'French (France)': {
        'name': 'French (France)',
        'lang': 'fr',
        'tld': 'fr'
    },
    'French (Canada)': {
        'name': 'French (Canada)',
        'lang': 'fr',
        'tld': 'ca'
    }
}

def lang_params(lang):
    '''
    Returns the parameters for the given language.
    '''
    if lang in languages:
        return languages[lang]['name'], languages[lang]['lang'], languages[lang]['tld']
    else:
        return False

# classes
class memo:
    '''
    Bot "memory"
    '''
    def __init__(self, engine=None):
        self.engine = engine
        self.load_mem()
    
    def create_mem(self):
        '''
        Create memory. Objects are pickle files.
        '''
        self.user_prefs = defaultdict(dict)
        if self.engine == None:
            if os.path.isdir('mem') == False:
                os.mkdir('mem')	
        else:
            self.df = pd.DataFrame(self.user_prefs)
        
        self.sync_mem()


    def load_mem(self):
        '''
        Load memory from mem folder. Objects are pickle files.
        '''
        if self.engine == None:
            if os.path.exists('mem/user_prefs.pkl'):
                with open('mem/user_prefs.pkl', 'rb') as f:
                    self.user_prefs = pickle.load(f)
            else:
                self.create_mem()
        else:
            try:
                self.df = pd.read_sql('SELECT * FROM user_prefs', self.engine)
                raw_user_prefs = self.df.to_dict(orient='index')
                self.user_prefs = defaultdict(dict)
                for key, value in raw_user_prefs.items():
                    self.user_prefs[value['index']] = {
                        'name': value['name'],
                        'lang': value['lang'],
                        'tld': value['tld']
                    }
            except:
                self.create_mem()

    def sync_mem(self):
        '''
        Sync memory with mem folder. Objects are pickle files.
        '''
        if self.engine == None:
            with open('mem/user_prefs.pkl', 'wb') as f:
                pickle.dump(self.user_prefs, f)
        else:
            self.df = pd.DataFrame.from_dict(self.user_prefs, orient='index')
            self.df.to_sql('user_prefs', self.engine, if_exists='replace', index=True)
