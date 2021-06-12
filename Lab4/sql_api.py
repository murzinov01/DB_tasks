import sqlite3
from tabulate import tabulate as tb
import os


def check_db(name):
    """
    This function is to check db existence
    """
    directory = os.getcwd()
    if os.path.exists(directory + "/" + name):
        print("Loading Student DB")
    else:
        print("Creating Student DB")


def print_tb(table):
    """
    This function is to print table
    """
    print(tb(table, tablefmt="fancy_grid"))


class StudentDB:
    """
    Class for work with Student DB
    """
    def __init__(self, name="students_db.sqlite"):
        check_db(name)
        self.__def_groups = ['19SE-1', '19SE-2', '19SE-3']
        self.__def_teachers = ['Bychkov', 'Semin', 'Leikin']
        self.__def_subjects = ['Algorithms', 'DB', 'Java']
        self.__def_teachers = ['']
        self.db_connection = sqlite3.connect(name, check_same_thread=False)
        self.db_cursor = self.db_connection.cursor()

    def __crete_tables(self):
        """
        This function is to create main tables of the Student DB
        """
        # Students table
        self.db_cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Students
            (id INTEGER PRIMARY KEY,
             name TEXT,
             course INTEGER NOT NULL,
             group_id INTEGER NOT NULL,
             teacher_id INTEGER NOT NULL,
             foreign key (group_id) references StudentGroups(id),
             foreign key (teacher_id) references Teachers(id)
            )
            ''')
        # Teachers table
        self.db_cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Teachers
            (id INTEGER PRIMARY KEY,
             name TEXT UNIQUE,
             subject TEXT
            )
            '''
        )
        # Groups table
        self.db_cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS StudentGroups
            (id INTEGER PRIMARY KEY,
             students_num INTEGER NOT NULL,
             group_name TEXT
            )
            '''
        )
        # create index
        self.db_cursor.execute(
            '''
            CREATE UNIQUE INDEX idx_groups
            ON StudentGroups (group_name) 
            '''
        )

    def save(self) -> int:
        """
        Save changes to DB file
        :return 1 - success, (-1) - error
        """
        self.db_connection.commit()
        print("Student DB saved")
        return 1

    def __insert_default_data(self):
        """
        This function is to insert default data to the tables
        """
        for index, name in enumerate(self.__def_groups):
            val = (index, name, 0)
            self.db_cursor.execute(
                '''
                INSERT INTO StudentGroups
                VALUES (?, ?, ?)
                ''', val
            )

        for index, name in enumerate(self.__def_teachers):
            val = (index, name, self.__def_subjects[index])
            self.db_cursor.execute(
                '''
                INSERT INTO Teachers
                VALUES (?, ?, ?)
                ''', val
            )

    def insert_student(self, info: tuple):
        """

        :param info: - tuple (name, course, group_name, teacher_name)
        """
        if info[0] < 1 or info[0] > 5:
            return -3

        group_id = self.get_group_id(info[2])
        if group_id == -1:
            return -1
        teacher_id = self.get_group_id(info[3])
        if teacher_id == -1:
            return -2
        val = (str(info[0]), int(info[1]), group_id, teacher_id)
        self.db_cursor.execute(
            '''
            INSERT INTO Students
            VALUES ((SELECT MAX(id) from Students) + 1, ?, ?, ?, ?)
            ''', val
        )
        if self.get_student_id(info[0]):
            return True
        return False

    def insert_teacher(self, info: tuple) -> bool:
        """

        :param info: - tuple (name, subject)
        """
        val = (info[0], info[1])
        self.db_cursor.execute(
            '''
            INSERT INTO Teachers
            VALUES ((SELECT MAX(id) from Teachers) + 1, ?, ?)
            ''', val
        )
        if self.get_teacher_id(info[0]):
            return True
        return False

    def insert_group(self, info: tuple) -> bool:
        """

        :param info: - tuple (name)
        """
        val = (info[0], 0)
        self.db_cursor.execute(
            '''
            INSERT INTO StudentGroups
            VALUES ((SELECT MAX(id) from StudentGroups) + 1, ?, ?)
            ''', val
        )
        if self.get_group_id(info[0]):
            return True
        return False

    def get_group_id(self, group_name) -> int:
        group_id = self.db_cursor.execute(
            '''
            SELECT id FROM StudentGroups WHERE name = ?
            ''', (group_name, )
        ).fetchall()
        if len(group_id) == 0:
            return -1
        return group_id[0][0]

    def get_teacher_id(self, teacher_name) -> int:
        teacher_id = self.db_cursor.execute(
            '''
            SELECT id FROM Teachers WHERE name = ?
            ''', (teacher_name, )
        ).fetchall()
        if len(teacher_id) == 0:
            return -1
        return teacher_id[0][0]

    def get_student_id(self, student_name) -> int:
        student_id = self.db_cursor.execute(
            '''
            SELECT id FROM Students WHERE name = ?
            ''', (student_name, )
        ).fetchall()
        if len(student_id) == 0:
            return -1
        return student_id[0][0]
