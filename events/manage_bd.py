from bd.CRUD import *
from bd.entities import *
from utils.utils import *
from sqlalchemy.exc import StatementError
import numpy as np

def update_bd(values):
    try:
        
        name_column = [col.name for col in OBTT.__table__.columns][1:]
        params = {name_column[i]: value for i, value in enumerate(values)}
        
        create_obtt(**params)

    except StatementError:
        raise ValueError
    

def search_by_value(id, value):
    results = search_obtt_by_value(column_name=id, value=value)
    attrs = [col.name for col in OBTT.__table__.columns]
    rows = [[getattr(res, attr) for attr in attrs] for res in results]

    return np.array(rows)


def Obtt(name):

    names, name_id  = get_name()
    id = name_id[names.index(name)]
    result = read_obtt(id)
    attrs = [col.name for col in OBTT.__table__.columns]
    params = [getattr(result, attr) for attr in attrs]

    return params    
    


    