import os

from flask import Flask, redirect, url_for, request

import pages
import db_wrapper

NAME = "Support service"
HOST = 'localhost'
PORT = 5050
DEBUG = True
BASE = 'service.db'
TEMPLATE_FOLDER = os.path.abspath('src/templates/')
STATIC_FOLDER = os.path.abspath('src/static')

db = db_wrapper.Database(BASE)

app = Flask(NAME,
            template_folder=TEMPLATE_FOLDER,
            static_folder=STATIC_FOLDER,
            )

page = pages.Pages()

@app.route("/")
def index():
    return redirect(url_for('new_ticket'))


@app.route('/new_ticket', methods=['GET', 'POST'])
def new_ticket():
    if request.method == 'POST':
        db.addTicket(
            request.form['username'],
            request.form['topic'],
            request.form['description']
            )
        
        ticketId = db.getLastID()
        return redirect(url_for('ticket') + '?number=' + ticketId)
    
    return page.new_ticket(title='Новое обращение')
    

@app.route('/ticket')
def ticket():
    ticketNumber = str(request.args.get('number'))
    activeTicket = db.getTicket(ticketNumber)
    
    return page.ticket(title='Статус обращения', data=activeTicket)
    
    
@app.route('/manager', methods=['GET', 'POST'])
def manager():
    if request.method == 'POST':
        for key in request.form:
            ticketNumber = key
            response = request.form['response']
            db.addResponseAndChangeStatus(ticketNumber, response)
            
            
    
    tickets = db.getOpenTickets()
    return page.manager(title='Открытые обращения', openTickets=tickets)


if __name__ == "__main__":
    app.run(host = HOST, port = PORT, debug = DEBUG)