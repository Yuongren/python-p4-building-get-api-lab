from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# GET /bakeries → all bakeries as JSON
@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in all_bakeries])

# GET /bakeries/<int:id> → single bakery with nested baked_goods
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    # Include baked_goods in nested list
    bakery_dict = bakery.to_dict()
    bakery_dict['baked_goods'] = [bg.to_dict() for bg in bakery.baked_goods]
    return jsonify(bakery_dict)

# GET /baked_goods/by_price → baked goods sorted by price descending
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([bg.to_dict() for bg in baked_goods])

# GET /baked_goods/most_expensive → single most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    bg = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if bg:
        return jsonify(bg.to_dict())
    return jsonify({}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)