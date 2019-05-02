from api.core.fabrics import create_database_fabric


db = create_database_fabric()


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    channel = db.Column(db.String(255))
    country = db.Column(db.String(255))
    os = db.Column(db.String(255))
    impressions = db.Column(db.Integer)
    clicks = db.Column(db.Integer)
    installs = db.Column(db.Integer)
    spend = db.Column(db.Numeric(12,2))
    revenue = db.Column(db.Numeric(12,2))
