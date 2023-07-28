from flask.views import MethodView
from flask_smorest import Blueprint, abort

bp = Blueprint(
    "Quotes", __name__,
    url_prefix='/v1/quotes',
)

@bp.route('/')
class GetQuotes(MethodView):
    def post(self):

        return {
            'success': True,
            'message': "Hello world"
        }