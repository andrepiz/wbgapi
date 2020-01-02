
'''Access information about World Bank lending groups
'''
import wbgapi as w
import builtins

def list(id='all'):
    '''Return a list of lending groups

    Parameters:
        id:         a lending group identifier or list-like of identifiers

    Returns:
        a generator object

    Example:
        lendingGroups = {row['id']: row['value'] for row in wbapi.lending.list()}
    '''

    url = '{}/{}/lendingtype/{}'.format(w.endpoint, w.lang, w.queryParam(id))
    for row in w.fetch(url):
        yield row

def get(id):
    '''Retrieve the specified lending group

    Parameters:
        id:         the lending group ID

    Returns:
        a lending group object

    Example:
        print(wbgapi.lending.get('IBD')['value'])
    '''
    
    url = '{}/{}/lendingtype/{}'.format(w.endpoint, w.lang, w.queryParam(id))
    return w.get(url)

def members(id):
    '''Return a set of economy identifiers that are members of the specified lending group

    Parameters:
        id:     a lending group identifier

    Returns:
        a set object of economy identifiers

    Notes:
        the returned members may not match the economies in the current database since we access the universal region lists from the API
    '''

    return w.region.members(id, 'lendingtype')

def Series(id='all',name='LendingGroupName'):
    '''Return a pandas Series object for the requested lending groups

    Parameters:
        id:         a lending group identifier or list-like of identifiers

        name:       the Series column name

    Returns:
        a pandas Series object
    '''

    return w.pandasSeries(builtins.list(list(id)), name=name)

def info(id='all'):
    '''Print a user report of lending groups

    Parameters:
        id:         a lending group identifier or list-like of identifiers

    Returns:
        None
    '''

    w.printInfo(builtins.list(list(id)))
