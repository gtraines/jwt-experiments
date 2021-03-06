from flask import Flask, jsonify, request, make_response, render_template
from flask_cors import CORS
import jwt
import datetime
from functools import wraps


app = Flask(__name__, static_folder='./public', static_url_path='')
app.config['SECRET_KEY'] = 'thisisthesecretkey'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        try:
            if not token:
                raise Exception()
            
            data = jwt.decode(token, app.config['SECRET_KEY'])

        except:
            return jsonify({'message': 'Token is missing or invalid'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/register', methods=['POST'])
def post_register():
    
    return render_template('sign-up/confirmation.html')

@app.route('/unprotected')
def unprotected():
    return 'this is unprotected'

@token_required
@app.route('/protected')
def protected():
    return 'this is protected'

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({
            'user': auth.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            })
        return jsonify({token: token.decode('UTF-8')})
    
    return make_response('Could not verify:',
                             401,
                             {'WWW-Authenticate' : "Basic realm='Login Required'"})


if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)

