from pyunifi.controller import Controller
from flask import Flask
from flask import jsonify
import json 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

app = Flask(__name__)
app.secret_key = 'ewfsdfwefs4d56f4sa1bre5g4gw'

def connect_controller():
    with open('/data/options.json', "r") as read_file:
        data = json.load(read_file)

    return Controller(data["ControllerURL"], data["Login"]["Username"], data["Login"]["Password"],data["Port"],data["Version"],data["SiteID"],data["ValidSSL"])

@app.route('/')
def main_page():
    c = connect_controller()
    vouchers =  c.list_vouchers()
    for v in vouchers:
        v["duration"]=(int(v["duration"])/60)
        if v["status"] == "VALID_MULTI":
            if v["quota"] == 0:
                v["status"] = "VALID_MULTI (unlimited)"
            else:
                v["status"] = "VALID_MULTI ("+str(v["quota"])+" usages)"
    return render_template('tickets/index.html', vouchers=vouchers)

@app.route('/create_tickets', methods=('GET', 'POST'))
def create_tickets():
    if request.method == 'POST':
            quantity = request.form['quantity']
            duration = request.form['duration']
            max_usage = request.form['max_usage']
            error= None

            if quantity is None:
                error = 'Incorrect quantity.'
            elif duration is None:
                error = 'Incorrect duration.'
            elif max_usage is None:
                error = 'Incorrect Max Usage'
            if error is None:
                c = connect_controller()
                c.create_voucher(int(quantity), max_usage, int(duration)*60)
                flash('Ticket(s) created')
                return render_template('tickets/create.html')


            flash(error)

    return render_template('tickets/create.html')

@app.route("/_delete_voucher", methods=('GET', 'POST'))
def delete_voucher():
    if request.method == 'POST':

        id = request.form['id']
        c = connect_controller()
        c.delete_voucher(id)
        return jsonify(status="success")
        
    return jsonify(status="error")

