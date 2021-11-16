import os
import firebase_admin
from datetime import datetime
from firebase_admin import credentials, db

cred = credentials.Certificate({
    "type": os.getenv('GCP_TOKEN_TYPE'),
    "project_id": os.getenv('GCP_PROJECT_ID'),
    "private_key_id": os.getenv('GCP_PRIVATE_KEY_ID'),
    "private_key": os.getenv('GCP_PRIVATE_KEY').replace(r'\n', '\n'),
    "client_email": os.getenv('GCP_CLIENT_EMAIL'),
    "client_id": os.getenv('GCP_CLIENT_ID'),
    "auth_uri": os.getenv('GCP_AUTH_URI'),
    "token_uri": os.getenv('GCP_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('GCP_AUTH_PROVIDER'),
    "client_x509_cert_url": os.getenv('GCP_CLIENT_CERT')
})

firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('DB_URL') 
})

class DBConnection():

    def __init__(self):
        self.nwdb = db.reference()

    def new_event(self, msg, evn_type, author, loc, date, time):
        ''' Creates a new event '''
        fmt_date = date + f'/{datetime.now().year}'

        new_event = self.nwdb.child('event').child(str(msg))
        new_event.update({
            'type': evn_type,
            'author_id': author,
            'date': fmt_date,
            'time': time,
            'location': loc
        })

    def get_event(self):
        events = self.nwdb.child('event')
        return events.get()

    def get_specific_event(self, id):
        events = self.nwdb.child('event')
        fetch_data = events.get()
        return fetch_data[id]

    def get_author(self, msg):
        ''' Fetches the authors member id '''
        event = self.nwdb.child('event').child(str(msg))
        fetch_data = event.get()
        event_type = fetch_data['type']
        author = fetch_data['author_id']
        return event_type, author
    
    def get_attendee(self, msg):
        ''' Fetches attendees for an event '''
        get_attendees = self.nwdb.child('event').child(str(msg))
        fetch_data = get_attendees.get()
        if 'None' in fetch_data['attendees']:
            return ['None']
        else:
            attendees = [member for member in fetch_data['attendees']]
            return attendees

    def add_attendee(self, msg, member):
        ''' Inserts attendees for an event '''
        inv_event = self.nwdb.child('event').child(str(msg))
        inv_event.update({'attendees': member})

    def rem_attendee(self, msg, member):
        ''' Removes an attendee from an event '''
        inv_event = self.nwdb.child('event').child(str(msg)).child('attendees')
        fetch_data = inv_event.get()
        attendees = [m for m in fetch_data]
        attendees.remove(member)
        inv_event.set(attendees)

    def del_event(self, event_id):
        events = self.nwdb.child('event')
        fetch_data = events.get()
        
        if str(event_id) in fetch_data:
            fetch_data.pop(str(event_id))

        new_data = fetch_data
        events.set(new_data)
        

        


