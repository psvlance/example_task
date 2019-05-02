from flask import jsonify

from api.api.models import Table
from api.api.schemas import (
    item_schema,
    items_schema
)

from api.api.app import api


@api.route("/",  methods=('GET', ))
def users():
    all_users = Table.all()
    result = items_schema.dump(all_users)
    return jsonify(result.data)
    # OR
    # return users_schema.jsonify(all_users)


@api.route("/<id>", methods=('GET', ))
def user_detail(id):
    user = Table.get(id)
    return item_schema.jsonify(user)