"""
While true, each time gets query on all
    Iterate through each user, check how much to generate
    send a request to query, if db does not contain anything generate 7 days -> write records
                             if db has several records generate for specific days -> write the records if they are not present else continue
                             if db has all the record skip user 
"""
import threading
from datetime import datetime, timedelta

import mysql
import requests
import numpy as np
from mysql.connector import Error


EXERCISE_INDEX_MAPPER = {
    0: 'Push-ups',
    1: 'Squats',
    2: 'Bridge',
    3: 'Push-ups',
    4: 'Squats',
    5: 'Bridge',
    6: 'Push-ups',
    7: 'Squats',
    8: 'Bridge',
    9: 'Push-ups'
}


def parse_schedule_request(data):

    user_schedule_request = {}

    user_schedule_request['user-id'] = data['user-id']
    user_schedule_request['generation-date'] = data['generation-date']
    schedule = data['user-data'][3:]
    idx_exercises = np.where(np.array([bool(eval(elem)) for elem in schedule]) == True)[0]
    user_schedule_request['exercise_1'] = EXERCISE_INDEX_MAPPER[idx_exercises[0]]
    user_schedule_request['count_1'] = schedule[idx_exercises[0]]
    user_schedule_request['exercise_2'] = EXERCISE_INDEX_MAPPER[idx_exercises[1]]
    user_schedule_request['count_2'] = schedule[idx_exercises[1]]
    if len(idx_exercises) > 2:
        user_schedule_request['exercise_3'] = EXERCISE_INDEX_MAPPER[idx_exercises[2]]
        user_schedule_request['count_3'] = schedule[idx_exercises[2]]
        return user_schedule_request
    
    user_schedule_request['exercise_3'] = 'No exercise'
    user_schedule_request['count_3'] = 0
    return user_schedule_request

class MySQLQuery:
    def __init__(self, host, username, password, db_name) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.db_name = db_name

        self.connection = self.connect()

    def connect(self):
        connection = None

        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                passwd=self.password,
                database=self.db_name
            )
            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Connection to MySQL database established.')
        except Error as err:
            print(f'{datetime.now().strftime("%H:%M:%S")} [Error] {err}')

        return connection

    def query(self, query_command):
        cursor = self.connection.cursor()
        result = None

        try:
            # print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Query MySQL database with the provided string.')
            cursor.execute(query_command)
            result = cursor.fetchall()

            return result
        except Error as err:
            print(f"Error: '{err}'")


class ScheduleWriter:
    def __init__(self, mysql_host, mysql_username, mysql_password, mysql_db_name, gateway_url) -> None:
        self.gateway_url = gateway_url
        self.__user_physical_table_query = """SELECT user_id, goal, level FROM fitnessapp.user_physical_information;"""
        # self.__exercise_table_query = """select * from fitnessapp.exercises WHERE user_id = 1 AND `datetime` >= '2023-05-02' AND `datetime` <= '2023-06-02';"""
        self.user_list = []
        self.lock = threading.Lock()

        self.mysql_query = MySQLQuery(host=mysql_host, username=mysql_username, password=mysql_password, db_name=mysql_db_name)

    def get_datetime(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_date = datetime.strptime(f"{current_date} 00:00:00", '%Y-%m-%d %H:%M:%S')
        generation_date = current_date + timedelta(days=1)
        return generation_date

    def write(self):
        print('write')
        # while True:

        # one_week_window = [current_date + timedelta(days=idx) for idx in range(1, 8)]
        generation_date = self.get_datetime()

        self.lock.acquire()
        users_data = self.mysql_query.query(self.__user_physical_table_query)
        self.lock.release()

        if users_data:
            for user in users_data:

                user_id, user_goal, user_level = user[0], user[1], user[2]
                exercise_query = f"""select * from fitnessapp.exercises WHERE 
                                    user_id = {user_id} AND `datetime` = '{generation_date.strftime("%Y-%m-%d %H:%M:%S")}'"""
                
                self.lock.acquire()
                user_exercise_schedules = self.mysql_query.query(exercise_query)
                self.lock.release()

                if (not user_exercise_schedules) and (user_id not in self.user_list):
                    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Queue the user to generation schedule.')

                    response = requests.post(self.gateway_url + '/generate', 
                                            data={'generation-date': generation_date, 'user-id': user_id, 'user-goal': user_goal, 'user-level': user_level})
                    
                    # if response.status_code == 200:
                    self.lock.acquire()
                    self.user_list.append([user_id, generation_date])
                    self.lock.release()

                    
    def read(self):
        print('read')
        print(self.user_list)
        if self.user_list:

            for user_info in self.user_list:

                response = requests.post(self.gateway_url + '/read', 
                        data={'generation-date': user_info[1], 'user-id': user_info[0]})

                if response.status_code == 200:
                    response_json = response.json()
                    print(response_json)
                    parsed_response = parse_schedule_request(response_json)
                    print('insert')
                    print(response_json)
                    insert_query = f"""
                        INSERT INTO fitnessapp.exercises 
                        (user_id, datetime, exercise_1, count_1, exercise_2, count_2, exercise_3, count_3) 
                        VALUES 
                        ({parsed_response['user-id']}, '{parsed_response['generation-date']}', 
                        '{parsed_response['exercise_1']}', {parsed_response['count_1']},
                        '{parsed_response['exercise_2']}', {parsed_response['count_2']},
                        '{parsed_response['exercise_3']}', {parsed_response['count_3']}
                        );
                    """
                    self.lock.acquire()
                    self.mysql_query.query(insert_query)
                    self.mysql_query.connection.commit()
                    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Inserted to database.')
                    self.lock.release()

                    try:
                        self.lock.acquire()
                        self.mysql_query.query(insert_query)
                        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Inserted to database.')
                        self.lock.release()
                    except Exception as ex:
                        print(f'{datetime.now().strftime("%H:%M:%S")} [ERROR] Cannot insert to database for user with user id {response["user-id"]}.')
                    
                    self.lock.acquire()
                    self.user_list.remove(user_info)
                    self.lock.release()
                if response.status_code == 202:
                    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Inserted to database.')
                


    def start_schedule_generation_queue(self):
        while True:
            write_thread = threading.Thread(target=self.write(), args=())
            read_thread = threading.Thread(target=self.read(), args=())

            write_thread.daemon = True
            read_thread.daemon = True

            write_thread.start()
            read_thread.start()

schedule_writer = ScheduleWriter(
    mysql_host='127.0.0.1', 
    mysql_username='root', 
    mysql_password='Test2023-mysql-pl-claim!', 
    mysql_db_name='fitnessapp', 
    gateway_url='http://localhost:9040'
    )

schedule_writer.start_schedule_generation_queue()



