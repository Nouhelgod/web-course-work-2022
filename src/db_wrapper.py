
import sqlite3

    
class Database():
    def __init__(self, file: str):
        self.file = file
        self.cursor = sqlite3.connect(self.file, check_same_thread=False)
        self.status = [
            'ожидание',
            'обращение закрыто'
        ]
        self.emptyResponse = 'none'
        
        
    def addTicket(self, username: str, topic: str, description: str):
        sql = """insert into tickets (username, topic, description, response, status) values (?, ?, ?, ?, ?)"""

        try:
            self.cursor.execute(sql, 
                                [username,
                                topic,
                                description,
                                self.emptyResponse,
                                self.status[0]])
            self.cursor.commit()
        
        except(sqlite3.OperationalError):
            self.__createDatabase(self.file)
            self.__createTable(self.file)
            self.addTicket(username, topic, description)
        
        
    def getLastID(self):
        sql = 'select max(number) from tickets'
        id = self.cursor.execute(sql).fetchall()[0][0]
        return str(id)
    
    
    def getTicket(self, ticketNumber: str):
        response = {}
        sql = """select * from tickets where number=?"""
        ticket = self.cursor.execute(sql, (ticketNumber, )).fetchall()[0]
        
        response['ticketNumber'] = ticket[0]
        response['name'] = ticket[1]
        response['topic'] = ticket[2]
        response['description'] = ticket[3]
        response['response'] = ticket[4]
        response['status'] = ticket[5]
        
        return response
    

    def getOpenTickets(self):
        sql = """select number from tickets where status=?"""
        status = [self.status[0]]
        
        openTicketNumbers = self.cursor.execute(sql, status).fetchall()
        openTickets = [self.getTicket(number[0]) for number in openTicketNumbers]

        return openTickets
    
    
    def addResponseAndChangeStatus(self, ticketNumber: str, response: str):
        status = self.status[1]
        sql = """update tickets set response=?, status=? where number=?"""
        values = (response, status, ticketNumber)
        
        self.cursor.execute(sql, values)
        self.cursor.commit()


    def __createDatabase(self, databaseFileName: str):
        with open(databaseFileName, mode='w') as newDB:
            newDB.close()
            
            
    def __createTable(self, databaseFile: str):
        base = Database(databaseFile)
        sql = 'create table tickets (number integer primary key,' +\
        'username varchar(30),' +\
        'topic text, ' +\
        'description text, ' +\
        'response text, ' +\
        'status varchar(20))'
        
        base.cursor.execute(sql)
        base.cursor.commit()
        base.cursor.close()
