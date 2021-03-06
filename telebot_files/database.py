import sqlite3
from datetime import datetime
from datetime import date
import time
import threading

'''
CONSTANTS FOR EVENTS
'''
EVENT_ID = 0
EVENT_NAME = 1
START_DATE = 2
END_DATE = 3
COLLECTION_DATE = 4
START_TIME = 5
END_TIME = 6
EVENT_MESSAGE = 7

'''
CONSTANTS FOR USERS
'''
USER_ID = 0
USER_NAME = 1
NUSNET_ID = 2
HOUSE = 3
TELEGRAM_ID = 4
TELEGRAM_HANDLE = 5
WIN_COUNT = 6

'''
CONSTANTS FOR EVENTS_CUSTOM_CHOICES
'''
ECC_EVENT_ID = 0
CHOICE_HEADER = 1
CHOICE_NAME = 2

'''
USER_FEEDBACK
'''
UF_EVENT_ID = 0
UF_USER_ID = 1
FEEDBACK = 2

'''
CONSTANTS FOR EVENTS_JOINED
'''
EJ_USER_ID = 0
EJ_EVENT_ID = 1
EJ_TIMING = 2
EJ_ITEM_CHOSEN = 3

LOCK = threading.Lock()

class Database:

    '''
    Initializing database.db file and connecting to the file
    '''

    def __init__(self):
        self.con = sqlite3.connect(
            'database.db', check_same_thread=False)
        self.cur = self.con.cursor()

    '''
    Initializing commit function
    '''
    def commit(self):
      self.con.commit()

    '''
    Initializing tables which only needs to be called once at the start of the program
    '''

    def create_tables(self):
        try:
            self.cur.execute(
                '''CREATE TABLE Events(EventID integer primary key, EventName text, StartDate text, EndDate text, CollectionDate text, 
                    StartTime text, EndTime text, Message text)''')
            self.cur.execute(
                '''CREATE TABLE Users(UserID integer primary key, UserName text, NusnetId text, House text, TelegramId text, TelegramHandle text, WinCount integer)''')
            self.cur.execute(
                '''CREATE TABLE EventsJoined(UserID integer not null, EventID integer not null, Timing text, ItemChosen text,
                FOREIGN KEY(UserID) REFERENCES Users(UserID),
                FOREIGN KEY(EventID) REFERENCES Events(EventID))''')
            self.cur.execute(
                '''CREATE TABLE EventsCustomChoices(EventID integer not null, ChoiceHeader text, ChoiceName text,
                FOREIGN KEY(EventID) REFERENCES Events(EventID))''')
            self.cur.execute(
                '''CREATE TABLE UserFeedback(EventID integer not null, UserID integer not null, Feedback text,
                FOREIGN KEY(UserID) REFERENCES Users(UserID),
                FOREIGN KEY(EventID) REFERENCES Events(EventID))''')

            # for general feedback table
            # self.cur.execute('INSERT INTO Events(EventID, EventName, StartDate, EndDate, CollectionDate, StartTime, EndTime, Message) values (?,?,?,?,?,?,?,?)', 
            #                 ((-1, 'general', None, None, None, None, None, None)))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            return e

    '''
    SQLite queries for users table
    '''

    def insert_user(self, username, nusnet_id, house, telegram_id, telegram_handle, win_count):
        try:
            LOCK.acquire(True)
            ## if user's full name and nusnet_id exists, do not insert
            self.cur.execute("SELECT * FROM Users WHERE UserName=? AND NusnetId=? AND House=?", (username, nusnet_id, house,))
            if (len(self.cur.fetchall())):
                return False

            ## if telegram_id registered before, update all attributes of user
            self.cur.execute("SELECT * FROM Users WHERE TelegramId=?", (telegram_id,))
            rows = self.cur.fetchall()

            if (len(rows)):
                user_id = rows[0][USER_ID]
                # old_win_count = rows[0][WIN_COUNT]
                # self.cur.execute(
                # "DELETE FROM Users WHERE TelegramId=?", (telegram_id,))

                # ## update details of user
                # self.cur.execute("INSERT INTO Users(UserName, NusnetId, House, TelegramId, TelegramHandle, WinCount) VALUES(?,?,?,?,?,?)",
                #                 (username, nusnet_id, house, telegram_id, telegram_handle, old_win_count))  #possible to insert old_user_id here?
                # self.cur.execute("SELECT * FROM Users WHERE TelegramId=?", (telegram_id,))
                # rows = self.cur.fetchall()
                # new_user_id = rows[0][USER_ID]
                # self.cur.execute("UPDATE EventsJoined SET UserID=? WHERE UserID=?", (new_user_id, old_user_id))
                # # self.cur.execute("UPDATE user_feedback SET username=? WHERE telegram_id=?", (username, telegram_id))
                self.cur.execute("UPDATE Users SET UserName=?, NusnetId=?, House=?, TelegramId=?, TelegramHandle=? WHERE UserId=?", (username, nusnet_id, house, telegram_id, telegram_handle, user_id))
            else:
                self.cur.execute("INSERT INTO Users(UserName, NusnetId, House, TelegramId, TelegramHandle, WinCount) VALUES(?,?,?,?,?,?)",
                                (username, nusnet_id, house, telegram_id, telegram_handle, win_count))                

            self.con.commit()
            return True
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()       

    def delete_user(self, telegram_id):
        try:
            LOCK.acquire(True)
            self.cur.execute(
                "DELETE FROM Users WHERE TelegramId=?", (telegram_id,))
            self.con.commit()    
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()            

    def query_all_users(self):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Users")
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                arrayString.append(row)
            print(arrayString)
            return arrayString
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_user_name(self, telegram_id):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Users WHERE TelegramId=?", (telegram_id,))
            self.con.commit()
            rows = self.cur.fetchall()
            user_name = rows[0][USER_NAME]
            print(user_name)
            return user_name 
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_user_details(self, telegram_id):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Users WHERE TelegramId=?", (telegram_id,))
            self.con.commit()
            rows = self.cur.fetchall()
            user_details = rows[0]
            print(user_details)
            return user_details
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()
    
    def query_user_id(self, user_id):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
            self.con.commit()
            rows = self.cur.fetchall()
            if not (rows):
                return
            user_details = rows[0]
            return user_details
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    '''
    SQLite queries for events table
    '''
    
    def insert_event(self, name, start_date, end_date, collection_date, start_time, end_time, message, item_bool):
        try:
            LOCK.acquire(True)
            ## if event name exists, do not insert
            self.cur.execute("SELECT * FROM Events WHERE EventName=?",(name,))
            if (len(self.cur.fetchall())):
                return False

            self.cur.execute("INSERT INTO events(EventName, StartDate, EndDate, CollectionDate, StartTime, EndTime, Message) values (?,?,?,?,?,?,?)",
                             (name, start_date, end_date, collection_date, start_time, end_time, message,))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def delete_event(self, name):
        try:
            LOCK.acquire(True)
            self.cur.execute("DELETE FROM Events WHERE EventName=?", (name,))
            self.con.commit()
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_all_events(self):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events")
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                arrayString.append(row)
            print(arrayString)
            return arrayString
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_all_sign_up_events(self):
        today = date.today()
        dateToday = time.strptime(today.strftime("%Y/%m/%d"), "%Y/%m/%d")
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events")
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                dateStart = time.strptime(row[START_DATE], "%Y/%m/%d")
                dateEnd = time.strptime(row[END_DATE], "%Y/%m/%d")
                if (dateStart <= dateToday <= dateEnd):
                    arrayString.append(
                        row)
            print(arrayString)
            return arrayString
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_all_ongoing_events(self):
        today = date.today()
        dateToday = time.strptime(today.strftime("%Y/%m/%d"), "%Y/%m/%d")
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events")
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                dateStart = time.strptime(row[START_DATE], "%Y/%m/%d")
                dateEnd = time.strptime(row[COLLECTION_DATE], "%Y/%m/%d")
                if (dateStart <= dateToday <= dateEnd):
                    arrayString.append(
                        row)
            print(arrayString)
            return arrayString
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_all_future_events(self):
        today = date.today()
        dateToday = time.strptime(today.strftime("%Y/%m/%d"), "%Y/%m/%d")
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events")
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                dateStart = time.strptime(row[START_DATE], "%Y/%m/%d")
                if (dateToday < dateStart):
                    arrayString.append(row)
            print(arrayString)
            return arrayString
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_all_past_events(self):
        today = date.today()
        dateToday = time.strptime(today.strftime("%Y/%m/%d"), "%Y/%m/%d")
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events")
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                dateEnd = time.strptime(row[COLLECTION_DATE], "%Y/%m/%d")
                if (dateEnd < dateToday):
                    arrayString.append(row)
            print(arrayString)
            return arrayString
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_event_message(self, event_name):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            self.con.commit()
            rows = self.cur.fetchall()
            event_message = rows[0][EVENT_MESSAGE] # takes only one event
            print(event_message)
            return event_message
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_event_exist(self, event_name):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            self.con.commit()
            if (len(self.cur.fetchall())):
                return True
            return False
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_event_id(self, event_id): ## input: event_id, output: event_details
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventID=?", (event_id,))
            self.con.commit()
            rows = self.cur.fetchall()
            event_details = rows[0]
            return event_details
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    '''
    SQLite queries for events_joined table
    '''

    def insert_event_joined(self, event_name, username, telegram_id, telegram_handle, timing, item_chosen):
        try:
            LOCK.acquire(True)
            ## delete event user have signed up for and insert a new query
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            event_rows = self.cur.fetchall()
            if (event_rows):
                event_id = event_rows[0][EVENT_ID]
            else:
               return

            self.cur.execute("SELECT * FROM Users WHERE UserName=?", (username,))
            user_rows = self.cur.fetchall()
            if (user_rows):
                user_id = user_rows[0][USER_ID]

            else:
                return

            self.cur.execute("SELECT * FROM EventsJoined WHERE UserID=? AND EventID=?", (user_id, event_id, ))
            if (len(self.cur.fetchall())):
                self.cur.execute("DELETE FROM EventsJoined WHERE UserID=? AND EventID=?", (user_id, event_id))

            self.cur.execute(
                "INSERT INTO EventsJoined(EventID, UserID, Timing, ItemChosen) values (?,?,?,?)", (event_id, user_id, timing, item_chosen,))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def delete_event_joined(self, event_name):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            rows = self.cur.fetchall()
            if (rows):
                event_id = rows[0][EVENT_ID]
            else:
                return
            self.cur.execute(
                "DELETE FROM EventsJoined WHERE EventID=?", (event_id,))
            self.con.commit()
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def delete_event_joined2(self, telegram_id):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Users WHERE TelegramId=?", (telegram_id,))
            user_rows = self.cur.fetchall()
            if (user_rows):
                user_id = user_rows[0][USER_ID]
            else:
                return
            self.cur.execute(
                "DELETE FROM EventsJoined WHERE UserID=?", (user_id,)
            )
            self.con.commit()
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_all_events_joined(self):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM EventsJoined")
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                arrayString.append(row)
            print(arrayString)
            return arrayString
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()
    
    def query_event_joined(self, event_name, win_count): 
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            rows = self.cur.fetchall()
            if (rows):
                event_id = rows[0][EVENT_ID]
            else:
                return
            self.cur.execute("SELECT * FROM EventsJoined WHERE EventID=?", (event_id,))
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                user_id = row[EJ_USER_ID]
                self.cur.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
                user_entry = self.cur.fetchall()
                user_win_count = user_entry[0][WIN_COUNT]
                if (user_win_count == win_count):
                    arrayString.append(row)
                else:
                    continue
            print(arrayString)
            return arrayString
        except Exception as e:
            print(e)
            return e   
        finally:
            LOCK.release() 

    def query_user_choice(self, event_name, item_chosen, win_count):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            rows = self.cur.fetchall()
            if (rows):
                event_id = rows[0][EVENT_ID]
            else:
                return
            self.cur.execute("SELECT * FROM EventsJoined WHERE EventID=? AND ItemChosen=?", (event_id, item_chosen,))
            rows = self.cur.fetchall()
            arrayString=[]
            for row in rows:
                user_id = row[EJ_USER_ID]
                self.cur.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
                user_entry = self.cur.fetchall()
                user_win_count = user_entry[0][WIN_COUNT]
                if (user_win_count == win_count):
                    arrayString.append(row)
                else:
                    continue
            print(arrayString)
            return arrayString
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_number_user_joined(self, event_name, timing):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            rows = self.cur.fetchall()
            if (rows):
                event_id = rows[0][EVENT_ID]
            else:
                return
            self.cur.execute("SELECT * FROM EventsJoined WHERE EventID=? AND Timing=?", (event_id, timing,))
            rows = self.cur.fetchall()
            userNumber = len(rows)
            print(userNumber)
            return userNumber
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release() 

    '''
    SQLite queries for events_custom_choices table
    '''
    def insert_events_custom_choices(self, event_name, choice_header, choice_name):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            rows = self.cur.fetchall()
            if (rows):
                event_id = rows[0][EVENT_ID]
            else:
                return
            self.cur.execute(
                "INSERT INTO EventsCustomChoices(EventID, ChoiceHeader, ChoiceName) values (?,?,?)", (event_id, choice_header, choice_name,))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def delete_events_custom_choices(self, event_name):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            rows = self.cur.fetchall()
            if (rows):
                event_id = rows[0][EVENT_ID]
            else:
                return
            self.cur.execute(
                "DELETE FROM EventsCustomChoices WHERE EventID=?", (event_id,))
            self.con.commit()
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_events_choices(self, event_name):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            rows = self.cur.fetchall()
            if (rows):
                event_id = rows[0][EVENT_ID]
            else:
                return
            self.cur.execute("SELECT * FROM EventsCustomChoices WHERE EventID = (?)", (event_id,))
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                arrayString.append(row)
            print(arrayString)
            return arrayString
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def query_event_choice_exist(self, event_name):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            rows = self.cur.fetchall()
            if (rows):
                event_id = rows[0][EVENT_ID]
            else:
                return
            self.cur.execute("SELECT * FROM EventsCustomChoices WHERE EventID=?", (event_id,))
            rows = self.cur.fetchall()
            if (rows):
                return True
            return False
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()
            

    '''
    SQLite queries for user_feedback table
    '''

    def insert_user_feedback(self, event_name, username, feedback):
        try:
            LOCK.acquire(True)
            # query events table for event id
            self.cur.execute("SELECT * FROM Users WHERE UserName=?", (username,))
            user_rows = self.cur.fetchall()
            if (user_rows):
                user_id = user_rows[0][USER_ID]
            else:
                return
            if (event_name == 'general'):
                self.cur.execute("INSERT INTO UserFeedback(EventID, UserID, Feedback) values (?,?,?)", (-1, user_id, feedback,))
                self.con.commit()
            else: 
                self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
                event_rows = self.cur.fetchall()
                if (event_rows):
                    event_id = event_rows[0][EVENT_ID]
                else:
                    return
                self.cur.execute("INSERT INTO UserFeedback(EventID, UserID, Feedback) values (?,?,?)", (event_id, user_id, feedback,))
                self.con.commit()
            return True
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def delete_user_feedback(self, event_name):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
            event_rows = self.cur.fetchall()
            if (event_rows):
                event_id = event_rows[0][EVENT_ID]
            else:
                return
            self.cur.execute(
                "DELETE FROM UserFeedback WHERE EventID=?", (event_id,))
            self.con.commit()
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

    def delete_user_feedback2(self, telegram_id):
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Users WHERE TelegramId=?", (telegram_id,))
            user_rows = self.cur.fetchall()
            if (user_rows):
                user_id = user_rows[0][USER_ID]
            else:
                return
            self.cur.execute(
                "DELETE FROM UserFeedback WHERE UserID=?", (user_id,))
            self.con.commit()
            print(telegram_id)
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()
    
    def query_user_feedback(self, event_name):
        try:
            LOCK.acquire(True)
            if (event_name == 'general'):
                self.cur.execute("SELECT * FROM UserFeedback WHERE EventID =?", (-1,))
                rows = self.cur.fetchall()
            else:
                self.cur.execute("SELECT * FROM Events WHERE EventName=?", (event_name,))
                event_rows = self.cur.fetchall()
                if (event_rows):
                    event_id = event_rows[0][EVENT_ID]
                else:
                    return
                self.cur.execute("SELECT * FROM UserFeedback WHERE EventID =?", (event_id,))
                rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                arrayString.append(row)
            print(arrayString)
            return arrayString
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()


    '''
    SQLite queries for win_count
    '''
    def increase_wincount(self, telegram_id): ## adds 1 to wincount of user
        max_win_count = len(self.query_all_past_events())
        try:
            LOCK.acquire(True)
            self.cur.execute("SELECT * FROM Users WHERE TelegramId=?", (telegram_id,))
            print(telegram_id)
            user = self.cur.fetchall()
            user_id = user[0][USER_ID]
            win_count = user[0][WIN_COUNT]
            ## only increase win_count to max_win_count
            if (win_count < max_win_count):
                win_count += 1
                self.cur.execute("UPDATE Users SET WinCount=? WHERE UserId=?", (win_count, user_id,))
                self.con.commit()
            return True
        except Exception as e:
            print(e)
            return e
        finally:
            LOCK.release()

