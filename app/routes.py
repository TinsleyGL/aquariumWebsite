from app import app, db
from app.models import User,Post,Aquarium
from flask import request

@app.route('/')
@app.route('/index')
def index():
    return 'hello'

@app.route('/data', methods=['GET','POST'])
def receive_data():
    print (
        request.form.get('UserID'),
        request.form.get('Aquarium'),
        request.form.get('Temperature'),
        request.form.get('PH'),
        User.query.get(int(request.form.get('UserID')))
    )
    
    data = Aquarium (
        userAquarium = User.query.get(int(request.form.get('UserID'))),
        name = request.form.get('Aquarium'),
        temperature = request.form.get('Temperature'),
        ph = request.form.get('PH')
    )
    db.session.add(data)
    db.session.commit()
    
    return (request.form.get('PH'))

@app.route('/send', methods=['GET'])
def send_data():
    return 'hello'