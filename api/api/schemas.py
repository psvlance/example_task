from api.core.fabrics import create_marshmallow_fabric


ma = create_marshmallow_fabric()


class TableSchema(ma.Schema):
    class Meta:
        fields = (
            'date',
            'channel',
            'country',
            'os',
            'impressions',
            'clicks',
            'installs',
            'spend',
            'revenue',
        )

    _links = ma.Hyperlinks(
        {"self": ma.URLFor("item", id="<id>"), "collection": ma.URLFor("items")}
    )


item_schema = TableSchema()
items_schema = TableSchema(many=True)