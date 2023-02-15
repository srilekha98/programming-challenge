from flask import request, Blueprint
from helper.sql import Query

movement = Blueprint('movement', __name__,
                        template_folder='templates')

@movement.route("/movements")
def get_movements():
    q = Query()
    keys = q.get_schema("movement")
    movements = []
    resp, rc = q.execute("select * from movement;")
    if rc == 200:
        for item in resp:
            row = dict(zip(keys, item))
            movements.append({"origin_farm":item[6],"dest_farm":item[12],
                              "num_units":item[20],"reason":item[2]})
        q.close()
        return {"response": movements, "status": 200}
    q.close()
    return {"response": resp, "status": 400}


def get_prems(resp, rc):
    resp = []
    if rc == 200:
         for inner_list in resp:
            resp.extend(inner_list)
    return resp

@movement.route("/premIDs")
def get_prem_ids():
     q = Query()
     premises = []
     resp, rc = q.execute("select distinct new_originpremid from movement;")
     premises.extend(get_prems(resp, rc))
     resp, rc = q.execute("select distinct new_destinationpremid from movement;")
     premises.extend(get_prems(resp, rc))
     q.close()
     return {"response": resp, "status": 200}


@movement.route("/movements/{opremiseid}/{dpremiseid}")
def get_move_data(opremiseid, dpremiseid):
    q = Query()
    keys = q.get_schema("movement")
    movements_origin_prem = []
    statement = '''SELECT * FROM movement WHERE new_originpremid='{}' and new_destinationpremid='{}';'''.format(opremiseid,dpremiseid)
    resp, rc = q.execute_sql_statement(statement)
    if rc == 200:
        for item in resp:
            row = dict(zip(keys,item))
            movements_origin_prem.append(row)
        return {"response":movements_origin_prem, "status": 200}
    else:
        return {"response": resp, "status": 400}
