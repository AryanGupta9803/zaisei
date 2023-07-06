from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
import os
import requests
from datetime import datetime

app = Flask(__name__)

key = {
    "type": "service_account",
    "project_id": "zaisei-kuhaku",
    "private_key_id": "98bbc6089717aad2ed7896bc9c59ca690617aa99",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDW7e7M1lTnbBqS\nCjis50BiCHR4XydNkZrLzPLKKn4bHUUHWpE8nIyF+1iP7LIDf8Z5Mmm9BW4+Ws8a\nGsJvntsbErBxLBFgyViYhI1BNKK3leAmL3vvAN29BCBAyiL5Kfl67gTS+YGICJBE\nPRV4ekXbaOlvNBn87/6Osccj2VLv/ays64oanc+AeGLjTpIeJrbPedxOiIHQIPAP\n/uDfYzBGbQbtulmDMIJozEvIUtLUd6UNAlXfAGP+bhuj1r97Xlrm/X/YSJUOHzDo\ndfN5BQjzZjhvi/jOS587YbMfTTG3ptp/DadOSRCTQTy/awW5KAum3SLg0LluKWhQ\n04X8eUfTAgMBAAECggEAOBCd68n3IN0Wu0S2TwgNx+TLuQCdSIM0XXhLVwgpmBoV\nARuTajut/l831WdZckc49zF62qdZgCOBBZ64XJSUNCY2Z3cm21f6Z+Kf1EQONBSB\nAYT+b7SKov06CpyP7e4QmYwQLxaNvvX46AwFF0XSBi+CQRNWuh/Ch+eA+m180IQh\nysCtFEXMf1PEczYp/fYBvWmFZb9lNRdgeG5zwy2zIqb/HRelLRkL2ujhgDhs8rU/\nw3KucjigasRJke9GpUSN6wIEscew9dgeFbHnQ9gqNK65SkuRfnvK4TdFEHNPGDck\nZk7vibjSTsQ8uDGqwGO9UcnSncHE5V2zEVt4/nHELQKBgQDu5sluC4EexsScEb/P\nyRirQhaZJrQS6/I2eKhBc8Y0gHxbbe/EDH10NGJLev5Udsihsp6Y2tHLARSPEvxB\nBs8kZMDGpnzKDpelAyWfOSiFI0LFlIOr5O8I30bwQ/rx9qHPuZsRfca+XPLLUERr\nKjAKDM1bAKPwTIi/7G3PAzB4bQKBgQDmT+xl2ul+ylXOZWay4GEm1mDFmooEXnb0\nWtG7/XmQSXnVjeav9S/5oz0A6DMTNmUCMIlAZfkksp2RDg8se680Ho0zsMptOd6n\nxiL6k8XuqtR+tTGHaNJwtpgriqO18u1EnJ8dYrWMlQsOodOuoZcG5wWhHMtT+Ynz\nG4t3200ZPwKBgCrx98G9da+XoZ5Ano92oeWfUrqjN3mzSm46UFy7uCSV+ETjRVej\nuyWZiRXyfSen1rciidoGc/IfNpflnMz/sVrkdbcAFKyp5N636xptRvhv9z/XS7gp\nxkJ9CJ6GSeUXJc1WmyaQyppL0SV1P2dYRRx5Yqz6N34p8+c0VCUDeMIdAoGBAJ1g\nueoz9+AzBQVflxjeaKSwUzpUSsGHh4OcV7s9DweAnedG6v8L7XeJi1MGWHhlcApZ\n/j/qLqBcCX2ofMfp0KQtyFEtGnYe2D4PD7HorpVTWJco26pq/3oT29HND+dyE54R\n5EyhOevRoNejz1GCjAAkd11LnslIOHLOPLRvP7TjAoGAXicIVGYZ+DiOAl7iQf2o\n7XHKUjUi4fbDRthr8W5Gq3ik6bRmJgc19NFWW+yLDtmojPePm/Q2gy/2x+O1u6y5\npO//5rmcXbrnIweDvUXRVr6R54W35tUAdb740PycuLx/F+KkLUQt5B3Hp7xcS0cA\ny4PFravFq5YsWk9RGv6noro=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-534l6@zaisei-kuhaku.iam.gserviceaccount.com",
    "client_id": "100601294893308728097",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-534l6%40zaisei-kuhaku.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
  }

cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred)
db = firestore.client()

users_ref = db.collection('user-info')
company_ref = db.collection('company-info')
port_ref = db.collection('user-portfolio')

def check_user(users, passw):
    doc_ref = users_ref.document(users)
    doc = doc_ref.get()
    if doc.exists:
        details = doc.to_dict()
        if details['user-id'] == users and details['password'] == passw:
            return True
    return False

@app.route('/')
def base():
    date = datetime.now().strftime("%d/%m/%y")
    return jsonify({"now":date})


@app.route('/login/')
def baseLogin() :
    return jsonify({"success": False})


@app.route('/login/<string:users>/<string:passw>')
def login(users, passw):
    doc_ref = users_ref.document(users)
    doc = doc_ref.get()
    if doc.exists:
        details = doc.to_dict()
        if details['user-id'] == users and details['password'] == passw:
            return jsonify({"status": 'logged in'})
        else:
            return jsonify({"status": 'incorrect password'})
    else:
        return jsonify({"status": 'user does not exist'})


@app.route('/signup/<string:users>/<string:passw>')
def signup(users, passw) :
    doc_ref = users_ref.document(users)
    doc = doc_ref.get()
    if doc.exists:
        return jsonify({"status": 'user already exists'})

    data = {"user-id": users, "password": passw}
    users_ref.document(users).set(data)
    doc_ref = users_ref.document(users)
    doc = doc_ref.get()

    if doc.exists:
        return jsonify({"status": 'signup successful'})

    return jsonify({"status": 'signup unsuccessful'})

@app.route('/<string:users>/<string:old_passw>/reset-password/<string:passw>')
def reset_password(users, old_passw, passw) :
    doc_ref = users_ref.document(users)
    doc = doc_ref.get()
    if doc.exists:
        details = doc.to_dict()
        if details['user-id'] == users and details['password'] == old_passw:
            data = {"user-id": users, "password": passw}
            users_ref.document(users).set(data)
            return jsonify({"status": 'password updated'})
        else: 
            return jsonify({'status': 'wrong existing password'})
    return jsonify({'status': 'unkown error'})


@app.route('/<string:users>/<string:passw>/delete-account/')
def delete_account(users, passw):
    doc_ref = users_ref.document(users)
    doc = doc_ref.get()
    if doc.exists:
        details = doc.to_dict()
        if details['user-id'] == users and details['password'] == passw:
            doc_ref.delete()
            return jsonify({"status": 'account deleted'})
        else:
            return jsonify({"status": 'incorrect password'})
    else:
        return jsonify({"status": 'user does not exist'})

@app.route('/company-financials/<string:symbol>/')
def get_financials(symbol):
    doc_ref = company_ref.document(symbol)
    doc = doc_ref.get()
    if doc.exists:
        details = doc.to_dict()
        return jsonify(details)

    url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + symbol + '&apikey=SEG3HCAR2PT57BNC'
    r = requests.get(url)
    data = r.json()
    if data == {}:
            data_up = {'status': 'no data available'}
            company_ref.document(symbol).set(data_up)
            return jsonify(data_up)
    company_ref.document(symbol).set(data)
    return jsonify(data)

@app.route('/portfolio/risk/<int:amount>/<float:risk>/')
def generate_portfolio_risk(amount, risk):
    if risk < 5:
        data = {'Fixed Deposits': amount}
        return jsonify(data)
    if risk > 40:
        data = {'Adani Enterprises': amount}
        return jsonify(data)
    if amount < 10000000:
        data = {'AAPL': amount * 0.2, 'Adani Enterprises': amount * 0.2, 'Infosys': 0.2 * amount, 'Bonds': 0.2 * amount, 'Fixed Deposits': 0.2 * amount}
        return jsonify(data)
    return jsonify({'status': 'failed'})

@app.route('/portfolio/return/<int:amount>/<float:returns>/')
def generate_portfolio_returns(amount, returns):
    if returns < 5:
        data = {'Fixed Deposits': amount}
        return jsonify(data)
    if returns > 40:
        data = {'Adani Enterprises': amount}
        return jsonify(data)
    if amount < 10000000:
        data = {'AAPL': amount * 0.2, 'Adani Enterprises': amount * 0.2, 'Infosys': 0.2 * amount, 'Bonds': 0.2 * amount, 'Fixed Deposits': 0.2 * amount}
        return jsonify(data)
    return jsonify({'status': 'failed'})

@app.route('/portfolio/risk/<int:amount>/<int:risk>/')
def generate_portfolio_risk_int(amount, risk):
    if risk < 5:
        data = {'Fixed Deposits': amount}
        return jsonify(data)
    if risk > 40:
        data = {'Adani Enterprises': amount}
        return jsonify(data)
    if amount < 10000000:
        data = {'AAPL': amount * 0.2, 'Adani Enterprises': amount * 0.2, 'Infosys': 0.2 * amount, 'Bonds': 0.2 * amount, 'Fixed Deposits': 0.2 * amount}
        return jsonify(data)
    return jsonify({'status': 'failed'})

@app.route('/portfolio/return/<int:amount>/<int:returns>/')
def generate_portfolio_returns_int(amount, returns):
    if returns < 5:
        data = {'Fixed Deposits': amount}
        return jsonify(data)
    if returns > 40:
        data = {'Adani Enterprises': amount}
        return jsonify(data)
    if amount < 10000000:
        data = {'AAPL': amount * 0.2, 'Adani Enterprises': amount * 0.2, 'Infosys': 0.2 * amount, 'Bonds': 0.2 * amount, 'Fixed Deposits': 0.2 * amount}
        return jsonify(data)
    return jsonify({'status': 'failed'})


@app.route('/<string:users>/<string:passw>/portfolio/')
def user_portfolio(users, passw):
    login_det = check_user(users, passw)
    if login_det == True:
        doc_ref = port_ref.document(users)
        doc = doc_ref.get()
        if doc.exists:
            details = doc.to_dict()
            if details == {} :
                return jsonify({'status': 'please add your portfolio first'})
            return jsonify(details)
        else:
            return jsonify({'status': 'please add your portfolio first'})
    else:
        return jsonify({'status': 'please check user details'})     

@app.route('/<string:users>/<string:passw>/portfolio/add/<string:symbol>/<int:amount>/')
def add_user_portfolio(users, passw, symbol, amount):
    login_det = check_user(users, passw)
    if login_det == True:
        doc_ref = port_ref.document(users)
        doc = doc_ref.get()
        if doc.exists:
            details = doc.to_dict()
            if symbol in details.keys():
                return jsonify({'status': 'please use update to change a particular stock'})
            details[symbol] = amount
            port_ref.document(users).set(details)
            return jsonify({'status': 'portfolio updated'})
        data = {symbol : amount}
        port_ref.document(users).set(data)
        return jsonify({'status': 'portfolio updated'})
    else:
        return jsonify({'status': 'please check user details'})

@app.route('/<string:users>/<string:passw>/portfolio/update/<string:symbol>/<int:amount>/')
def update_user_portfolio(users, passw, symbol, amount):
    login_det = check_user(users, passw)
    if login_det == True:
        doc_ref = port_ref.document(users)
        doc = doc_ref.get()
        if doc.exists:
            details = doc.to_dict()
            if symbol in details.keys():
                details[symbol] = amount
                port_ref.document(users).set(details)
                return jsonify({'status': 'portfolio updated'})
            return jsonify({'status': 'please use add to add a new stock'})
        return jsonify({'status': 'please add a portfolio item first'})
    else:
        return jsonify({'status': 'please check user details'})

@app.route('/<string:users>/<string:passw>/portfolio/delete/<string:symbol>/')
def delete_user_portfolio(users, passw, symbol):
    login_det = check_user(users, passw)
    if login_det == True:
        doc_ref = port_ref.document(users)
        doc = doc_ref.get()
        if doc.exists:
            details = doc.to_dict()
            if symbol in details.keys():
                del(details[symbol])
                port_ref.document(users).set(details)
                return jsonify({'status': 'portfolio updated'})
            return jsonify({'status': 'item not present in portfolio'})
        return jsonify({'status': 'please add a portfolio item first'})
    else:
        return jsonify({'status': 'please check user details'})

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)

