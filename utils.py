import os
import pickle
import psycopg2
import pandas as pd
import sqlalchemy
from collections import defaultdict

# parameters
languages = {
    'English': {
        'lang': 'en',
        'tld': {
            'US': 'com',
            'UK': 'co.uk',
            'Australia': 'com.au',
            'Canada': 'ca',
            'New Zealand': 'co.nz',
            'South Africa': 'co.za',
            'India': 'in',
            'Ireland': 'ie',
        }
    },
    'Spanish': {
        'lang': 'es',
        'tld': {
            'Spain': 'es',
            'Mexico': 'com.mx',
            'US': 'com',
        }
    },
    'Portuguese': {
        'lang': 'pt',
        'tld': {
            'Brazil': 'com.br',
            'Portugal': 'pt',
        }
    },
    'French': {
        'lang': 'fr',
        'tld': {
            'France': 'fr',
            'Canada': 'ca',
        }
    }
}

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
                self.user_prefs = self.df.to_dict('index')
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
            self.df = pd.DataFrame(self.user_prefs)
            self.df.to_sql('user_prefs', self.engine, if_exists='replace', index=False)
