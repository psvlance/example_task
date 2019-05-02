from flask import url_for

from api.core.fabrics import (
    create_app_fabric,
    create_marshmallow_fabric,
    create_database_fabric,
    register_bps
)

from api.settings import settings

app = create_app_fabric(settings=settings)
ms = create_marshmallow_fabric()
db = create_database_fabric()

register_bps()


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    print(links)
    return '<br/>'.join(links[0])
