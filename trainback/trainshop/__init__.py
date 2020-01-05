from flask import Blueprint
from flask_restplus import Api

blueprint = Blueprint('shop_api', __name__, url_prefix='/shop')

api = Api(blueprint,
          title='TRAINBACK SHOP API',
          version='0.1',
          description='an api for the shop'
          )

# api.add_namespace()