import os
import pickle
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
    def __init__(self):

        self.load_mem()
    
    def create_mem(self):
        '''
        Create memory. Objects are pickle files.
        '''
        if os.path.isdir('mem') == False:
            os.mkdir('mem')	
        self.tts_mem = defaultdict(dict)
        self.sync_mem()

    def load_mem(self):
        '''
        Load memory from mem folder. Objects are pickle files.
        '''
        if os.path.exists('mem/tts_mem.pkl'):
            with open('mem/tts_mem.pkl', 'rb') as f:
                self.tts_mem = pickle.load(f)
        else:
            self.create_mem()

    def sync_mem(self):
        '''
        Sync memory with mem folder. Objects are pickle files.
        '''
        with open('mem/tts_mem.pkl', 'wb') as f:
            pickle.dump(self.tts_mem, f)
