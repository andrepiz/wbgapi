
'''Access information about World Bank databases

World Bank databases are multi-dimensional databases that at a minimum
have series, economy, and time dimensions. Concept names are not consistent
across databases, but the wbgapi module tries to insulate the user from
these inconsistencies. Additional (4th or 5th) dimensions are possible but are not currently
supported.
'''

import wbgapi as w
import urllib.parse
import builtins


# concepts cached per database
_concepts = {}
_metadata_flags = {}

def list(id='all'):
    '''Return a list of databases

    Arguments:
        id:     a database identifier or list-like

    Returns:
        a generator object

    Example:
        for elem in wbgapi.source.list():
            print(elem['id'], elem['name'], elem['lastupdated'])
    '''

    return w.fetch(_sourceurl(w.queryParam(id)), {'databid': 'y'})

def get(db=None):
    '''Retrieve the record for a single database

    Arguments:
        db:      the database ID (e.g., 2=WDI). Default to the global db

    Returns:
        a database object

    Example:
        print wbgapi.source.get(2)['name']
    '''

    return w.get(_sourceurl(db), {'databid': 'y'})

def concepts(db=None):
    '''Retrieve the concepts for the specified database. This is primarily
    used internally to provide a consistent interface

    Arguments:
        db:     the database ID (e.g., 2=WDI). Default to the global database

    Returns:
        a dictionary of concepts: keys are URL friendly

    Example:
        for k,v in wbgapi.source.concepts(2).items():
            print(k, v)
    '''

    global _concepts

    if db is None:
        db = w.db

    db = int(db)
    c = _concepts.get(db)
    if c is not None:
        return c

    url = '{}/{}/sources/{}/concepts'.format(w.endpoint, w.lang, db)
    c = {}
    for row in w.fetch(url, concepts=True):
        key = urllib.parse.quote(row['id']).lower()
        c[key] = row['value']

    _concepts[db] = c
    return c

def features(concept, id='all', db=None):
    '''Retrieve features for the specified database. This is an internal function
    called by list() in other modules.

    Arguments:
        concept:    the concept to retrieve (e.g., 'series')

        id:         object identifiers to retrieve; must be a well-formed string

        db:         the database to access (e.g., 2=WDI). Default uses the global database

    Returns:
        a generator object

    Example:
        for elem in wbgapi.source.features('time'):
            print(elem['id'], elem['value'])
    '''

    return w.fetch(_concepturl(concept, id, db))

def feature(concept, id, db=None):
    '''Retrieve a single feature for the specified database. This is an internal function
    called by get() in other modules.

    Arguments:
        concept:    the concept to retrieve (e.g., 'series')

        id:         the object ID

        db:         the database to access (e.g., 2=WDI). Default uses the global database

    Returns:
        a database object

    Example:
        print(wbgapi.source.feature('series', 'SP.POP.TOTL')['value'])
    '''

    return w.get(_concepturl(concept, id, db))

def has_metadata(db=None):
    '''Test whether the specified database is expected to have metadata, as determined
    by the database record returned from the API.

    Arguments:
        db:     the database to query. Pass None to reference the global database

    Returns:
        Boolean
    '''

    if db is None:
        db = w.db

    global _metadata_flags
    m = _metadata_flags.get(db)
    if m is None:
        src = get(db)
        m = src.get('metadataavailability','').upper() == 'Y'
        _metadata_flags[db] = m

    return m

def info(id='all'):
    '''Print a user report of databases

    Arguments:
        id:         a database identifier or list-like

    Returns:
        None
    '''
    
    w.printInfo(builtins.list(list(id)), value='name')

def _sourceurl(db):
    '''Internal function: returns the URL for fetching database objects
    '''

    if db is None:
        db = w.db

    return '{}/{}/sources/{}'.format(w.endpoint, w.lang, db)

def _concepturl(concept, id, db):
    '''Internal function: return the URL for fetching database features
    '''

    if db is None:
        db = w.db

    concept_list = concepts(db)
    if concept_list.get(concept) is None:
        return None

    return '{}/{}/sources/{}/{}/{}'.format(w.endpoint, w.lang, db, concept, id)

