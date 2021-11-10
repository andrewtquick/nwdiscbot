from datetime import datetime, timedelta

class Utils(object):

    def __init__(self, object):
        self.utils = object
    
    def convert_datetime(self, date, time):
        format = '%H:%M'
        est_time = (datetime.strptime(time, format)).strftime(format)
        cst_time = (datetime.strptime(time, format) - timedelta(hours=1)).strftime(format)
        mst_time = (datetime.strptime(time, format) - timedelta(hours=2)).strftime(format)
        pst_time = (datetime.strptime(time, format) - timedelta(hours=3)).strftime(format)

        return f'**{date}' + f'/{datetime.now().year}**' + f'\n-- {est_time} **EST**\n-- {cst_time} **CST**\n-- {mst_time} **MST**\n-- {pst_time} **PST**'

    def within_start(self, date, time):
        event_date = date + ' ' + time
        now = datetime.now()
        start_time = datetime.strptime(event_date, '%m/%d/%Y %H:%M')

        time_difference = (start_time - now) / timedelta(minutes=1)
        
        if time_difference < 30:
            return True
        else:
            return False

    def check_dt(self, date, time):
        event_date = date + ' ' + time
        now = datetime.now()
        start_time = datetime.strptime(event_date, '%m/%d/%Y %H:%M')

        if now <= start_time:
            return True
        else:
            return False