import shelve
import os
import json
import filelock as FileLock

KEY_VALUE_PATH = '/data/mbot/'    

def create_keyvalue_store(name):
    """Create a key value store"""
    
    # check if the key value store already exists
    if os.path.exists(KEY_VALUE_PATH + name):
        return False # key value store already exists

    # create the key value store
    with open(KEY_VALUE_PATH + name, 'w') as f:
        f.write("{}")

    return True

def check_keyvalue_store_exists(name):
    """Check if a key value store exists"""
    return os.path.exists(KEY_VALUE_PATH + name)

def get_keyvalue(name, key):
    """Get a key value"""
    
    print('get_keyvalue: ' + name + ' ' + key)

    # check if the key value store exists
    if not check_keyvalue_store_exists(name):
        return None

    with FileLock.FileLock(KEY_VALUE_PATH + name + '.lock'):
        # get the key value, if it exists.
        # otherwise return None
        with open(KEY_VALUE_PATH + name, 'r') as f:
            data = json.load(f)
            if key in data:
                return data[key]
            else:
                return None

def set_keyvalue(name, key, value):
    """Set a key value"""

    # check if the key value store exists
    if not check_keyvalue_store_exists(name):
        return False

    with FileLock.FileLock(KEY_VALUE_PATH + name + '.lock'):
        # set the key value
        with open(KEY_VALUE_PATH + name, 'r') as f:
            data = json.load(f)
            data[key] = value
        
        with open(KEY_VALUE_PATH + name, 'w') as f:
            json.dump(data, f)

    return True

def delete_keyvalue(name, key):
    """Delete a key value"""
    
    # check if the key value store exists
    if not check_keyvalue_store_exists(name):
        return False

    # delete the key value
    with FileLock.FileLock(KEY_VALUE_PATH + name + '.lock'):
        with open(KEY_VALUE_PATH + name, 'r') as f:
            data = json.load(f)
            if key in data:
                del data[key]
        
        with open(KEY_VALUE_PATH + name, 'w') as f:
            json.dump(data, f)
            
        
def get_all_keyvalues(name):
    """Get all key values"""
    
    # check if the key value store exists
    if not check_keyvalue_store_exists(name):
        return None

    shelve_data = {}

    # get all key values
    with FileLock.FileLock(KEY_VALUE_PATH + name + '.lock'):
        with open(KEY_VALUE_PATH + name, 'r') as f:
            shelve_data = json.load(f)
    
    return shelve_data

def delete_keyvalue_store(name):
    """Delete a key value store"""

    # check if the key value store exists
    if not check_keyvalue_store_exists(name):
        return False
    
    os.remove(KEY_VALUE_PATH + name)

    return True

    