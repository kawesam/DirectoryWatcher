import time
import os
import csv
import json
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# class to watch the changes in a given directory

class Watch :
    DIRECTORY = '/Users/samlinncon/Downloads/PythonWatcher'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(20)
        except :
            self.observer.stop()
        self.observer.join()


 # class to handle the event and record to db
class Handler(FileSystemEventHandler):
    #handle event when the file is created to call a REST api and insert
    @staticmethod
    def on_any_event( event):
        if event.event_type == 'created':
            #walk to parse the files
            for root, dirs, files in os.walk(event.src_path):
                for file in files:
                    print file

        elif event.event_type == 'modified':

            for root, dirs, files in os.walk(event.src_path):
                for file in files:
                    if file.endswith(".csv"):
                        users = []
                        with open(os.path.join(event.src_path,file),'rb') as f:
                           csvdocs = csv.reader(f,)
                           next(csvdocs)
                           for row in csvdocs:
                               #creates a list of the names
                               users.append(row[0])
                               # my_list = (row).split(",")
                               # print my_list

                        #iterate through each element of the list and send to REST API
                        for x in users:
                            data = {"names": x}
                            # data_json = json.dumps(data)
                            headers = {'Content-type': 'application/json'}
                            print data
                            r = requests.post("http://localhost:8000/api/csv_data", data=data)

                            print r

                    # else:
                    #     # print "None"




if __name__ == '__main__':
    w = Watch()
    w.run()





