from responses import *
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



api.add_resource(bonistas, '/api/arg/bonistas/<panel_id>')
api.add_resource(BCRA, '/api/arg/bcra')

api.add_resource(dolarHoy, '/api/arg/dolarHoy')
api.add_resource(mep, '/api/arg/mep')
api.add_resource(ccl, '/api/arg/ccl')

api.add_resource(options, '/api/arg/options')
api.add_resource(options_lanzamiento, '/api/arg/options/lanzamiento/<underlying>')

api.add_resource(argy_quots,'/api/arg/<panel_id>/<settlement_id>')



if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0')