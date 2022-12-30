from flask import render_template

class Pages():    
    def new_ticket(self, title: str):
        return render_template('new_ticket.html', title=title)
    
    def ticket(self, title: str, data: dict):
        return render_template('ticket.html', title=title, data=data)
    
    def manager(self, title: str, openTickets: list):
        return render_template('manager.html', title=title, openTickets=openTickets)