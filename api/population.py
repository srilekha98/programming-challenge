from flask import request, Blueprint
from helper.sql import Query

pop = Blueprint('pop', __name__,
                        template_folder='templates')


@pop.route("/population")
def get_movements():
    q = Query()
    keys = q.get_schema("population")
    pop_data = []
    resp, rc = q.execute("select * from population;")
    if rc == 200:
        for item in resp:
            row = dict(zip(keys,item))
            pop_data.append(row)
        q.close()
        return {"response": pop_data, "status": 200}
    q.close()
    return {"response": resp, "status": 400}
