from bd.CRUD import *
from bd.entities import *
from utils.utils import *
from sqlalchemy.exc import StatementError

def update_bd(values):
    try:
        
        name_column = [col.name for col in OBTT.__table__.columns][1:]
        params = {name_column[i]: value for i, value in enumerate(values)}
        print(params)
        
        new_obtt = create_obtt(**params)

    except StatementError:
        raise ValueError
    

def search_by_value(id, value):

    results = search_obtt_by_value(column_name=id, value=value)
    

    


    