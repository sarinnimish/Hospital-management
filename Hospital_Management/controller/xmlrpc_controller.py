import xmlrpc.client

url = 'http://localhost:8067'
db = 'test_db'
uid= 2
username = 'admin'
password = 'admin'

def get_odoo_version(url):
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        version_info = common.version()
        return version_info
    except Exception as e:
        return f'Error retrieving version information: {e}'



def authenticate_and_get_uid(url, db, username, password):
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        if uid is None:
            return 'Authentication failed'
        return uid
    except xmlrpc.client.Fault as fault:
        return f'Error during authentication: {fault}'
    except Exception as e:
        return f'Unexpected error during authentication: {e}'


def get_fields(url, db, username, password, model_name):
    try:
        uid = authenticate_and_get_uid(url, db, username, password)
        if isinstance(uid, str):
            return uid 
        
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        fields = models.execute_kw(db,uid,password,model_name, 'fields_get', [], {'attributes': ['string','type','required']})
        return fields
    except Exception as e:
        return f'Error retrieving fields: {e}'
    


def get_records(url, db,uid, password,):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    records=models.execute_kw(db, uid, password, 'hospital.management', 'search', [[['name', '=', "Nimish"]]])
    return records

def get_count(url, db, uid, password):
     models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
     count=models.execute_kw(db, uid, password, 'hospital.management', 'search_count', [[['name', '=', "Nimish"]]])
     return count

def get_read_records(db, uid, password):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    ids = models.execute_kw(db, uid, password, 'hospital.management', 'search', [[['name', '=', "Nimish"]]])
    [record] = models.execute_kw(db, uid, password, 'hospital.management', 'read', [ids])
    # count the number of fields fetched by default
    return len(record)

def create_records(url, db, uid, password, model_name):
    """Create a new record in the specified model."""
   
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    record_id = models.execute_kw(db, uid, password, model_name, 'create', [{'name': 'TestPartner', 'Insurance':'1','Blood_Type':'b+'}])
    return record_id
   
    

def update_records(url, db, uid, password, model_name):    
    # import pdb; pdb.set_trace()
  try:
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    partner=models.execute_kw(db, uid, password, model_name, 'write', [[record_id], {'name': 'Newerpartner','Blood_Type':'o+'}])
    partner=models.execute_kw(db, uid, password, 'hospital.management', 'read', [[record_id], ['display_name']])
    return f"Record Updated successfully with ID: {partner}"
  except Exception as e:
        return f"Error creating record: {e}"

def delete_records(url, db, uid, password,model_name):
#   import pdb; pdb.set_trace()
  try:
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    delete=models.execute_kw(db, uid, password, model_name, 'unlink', [[record_id]])
    return f"Record Deleted successfully with ID: {delete}"
  except Exception as e:
        return f"Error creating record: {e}"


version_info = get_odoo_version(url)
print(version_info)

uid = authenticate_and_get_uid(url, db, username, password)
print("Authenticated UID:", uid)

fields = get_fields(url, db, username, password, 'hospital.management')
print("Fields of hospital.management:", fields)

records = get_records(url, db, uid, password)
print("Records:", records)

count = get_count(url, db, uid, password)
print("Count Records:", count)

record= get_read_records(db, uid, password)
print("Read Records:", record)

record_id = create_records(url, db, uid, password, 'hospital.management')
print("create Records:",record_id)

partner= update_records(url, db, uid, password, 'hospital.management')
print("Updated Records:",partner)

delete= delete_records(url, db, uid, password,'hospital.management')
print("Delete Records:",delete)