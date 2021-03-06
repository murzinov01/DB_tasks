import sqlite3
from tabulate import tabulate as tb
import os


def check_db(name: str) -> bool:
    """
    This function is to check db existence
    """
    directory = os.getcwd()
    if os.path.exists(directory + "/" + name):
        print("Loading Student DB")
        return True
    else:
        print("Creating Student DB")
        return False


def print_tb(table):
    """
    This function is to print table
    """
    return str(tb(table, tablefmt="pipe"))


class StudentDB:
    """
    Class for work with Student DB
    """
    def __init__(self, name="students_db.sqlite", template='default_db'):
        self.name = name
        self.template = template
        self.created = check_db(name)
        self.__def_groups = ['19SE-1', '19SE-2', '19SE-3']
        self.__def_teachers = ['Bychkov', 'Semin', 'Leikin']
        self.__def_subjects = ['Algorithms', 'DB', 'Java']
        self.db_connection = sqlite3.connect(name, check_same_thread=False)
        self.db_cursor = self.db_connection.cursor()
        if not self.created:
            self.crete_tables()

    def crete_tables(self):
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
             name TEXT,
             students_num INTEGER NOT NULL
            )
            '''
        )
        # create index
        self.db_cursor.execute(
            '''
            CREATE UNIQUE INDEX idx_groups
            ON StudentGroups (name) 
            '''
        )
        self.insert_student_trigger()
        self.delete_student_trigger()
        if self.template == 'default_db':
            self.__insert_default_data()
        self.save()

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

    def insert_student_trigger(self):
        self.db_cursor.execute(
            '''
            CREATE TRIGGER student_insert
            AFTER INSERT ON Students
            BEGIN
                 UPDATE StudentGroups 
                 SET students_num = (students_num + 1)
                 WHERE id = NEW.group_id;
            END;
            '''
        )
        self.save()

    def delete_student_trigger(self):
        self.db_cursor.execute(
            '''
            CREATE TRIGGER student_delete
            AFTER DELETE ON Students
            BEGIN
                 UPDATE StudentGroups 
                 SET students_num = (students_num - 1)
                 WHERE id = OLD.group_id;
            END;
            '''
        )
        self.save()

    def insert_student(self, info: tuple):
        """
        :param info: - tuple (name, course, group_name, teacher_name)
        """
        if info[1] < 1 or info[1] > 5:
            return -3

        group_id = self.get_group_id(info[2])
        if group_id == -1:
            return -1
        teacher_id = self.get_teacher_id(info[3])
        if teacher_id == -1:
            return -2
        val = (str(info[0]), int(info[1]), group_id, teacher_id)
        self.db_cursor.execute(
            '''
            INSERT INTO Students
            VALUES ((SELECT MAX(id) from Students) + 1, ?, ?, ?, ?)
            ''', val
        )
        self.save()
        if self.get_student_id(info[0]) != -1:
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
        self.save()
        if self.get_teacher_id(info[0]) != -1:
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
        self.save()
        if self.get_group_id(info[0]) != -1:
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

    def check_student(self, student_id) -> int:
        student_id = self.db_cursor.execute(
            '''
            SELECT * FROM Students WHERE id = ?
            ''', (student_id,)
        ).fetchall()
        if len(student_id) == 0:
            return False
        return True

    def check_teacher(self, teacher_id) -> int:
        teacher_id = self.db_cursor.execute(
            '''
            SELECT * FROM Teachers WHERE id = ?
            ''', (teacher_id,)
        ).fetchall()
        if len(teacher_id) == 0:
            return False
        return True

    def _get_all_students(self):
        return self.db_cursor.execute(
                '''
                SELECT * FROM Students
                '''
            ).fetchall()

    def _get_all_teachers(self):
        return self.db_cursor.execute(
                '''
                SELECT * FROM Teachers
                '''
            ).fetchall()

    def _get_all_groups(self):
        return self.db_cursor.execute(
                '''
                SELECT * FROM StudentGroups
                '''
            ).fetchall()

    def delete_student(self, student_name=None, student_id=None):
        """
        :param student_name:
        :return:
        """
        if student_name is not None:
            student_id = self.get_student_id(student_name)
            if student_id == -1:
                return -1
            self.db_cursor.execute(
                '''
                DELETE FROM Students
                WHERE name = ?
                ''', (student_name,)
            )
            self.save()
            if self.get_student_id(student_name) == -1:
                return True
            return False
        elif student_id is not None:
            if self.check_student(student_id):
                self.db_cursor.execute(
                    '''
                    DELETE FROM Students
                    WHERE id = ?
                    ''', (student_id,)
                )
                self.delete_student_trigger()
                self.save()
                if self.check_student(student_id):
                    return False
                return True
            return -1

    def update_student_name(self, info: tuple):
        """
        :param info: tuple (student_id, new_name)
        """
        if not self.check_student(info[0]):
            return -1
        self.db_cursor.execute(
            '''
            UPDATE Students
            SET name = ?
            WHERE id = ?
            ''', (info[1], info[0])
        )
        student_id = self.get_student_id(info[0])
        self.save()
        if student_id == -1:
            return False
        return True

    def update_teacher_subject(self, info):
        """
        :param info: tuple (teacher_id, new_subject)
        :return:
        """
        if not self.check_teacher(info[0]):
            return -1
        self.db_cursor.execute(
            '''
            UPDATE Teachers
            SET subject = ?
            WHERE id = ?
            ''', (info[1], info[0])
        )
        st_id = self.find_teachers_by_subject(info[1])
        self.save()
        if st_id != -1:
            return True
        return False

    def find_teachers_by_subject(self, subject_name):
        teachers_data = self.db_cursor.execute(
            '''
            SELECT * FROM Teachers WHERE subject = ?
            ''', (subject_name,)
        ).fetchall()
        if len(teachers_data) == 0:
            return -1
        return teachers_data

    def find_students_by_group_name(self, group_name):
        """
        :param group_name:
        :return:
        """
        student_data = self.db_cursor.execute(
            '''
            SELECT Students.name, StudentGroups.name 
            FROM Students, StudentGroups
            WHERE StudentGroups.name = ?
            ''', (group_name, )
        ).fetchall()
        if len(student_data) == 0:
            return -1
        return student_data

    def show_db(self) -> str:
        result = "DataBase:\n\n"
        tables = self.db_cursor.execute(
            '''
            SELECT name FROM sqlite_master WHERE type = "table"
            '''
        ).fetchall()
        if len(tables) == 0:
            return result
        if len(tables) == 3:
            result += "Students\n" + print_tb(self._get_all_students()) + "\n"
        result += "Teachers\n" + print_tb(self._get_all_teachers()) + "\n"
        result += "Groups\n" + print_tb(self._get_all_groups()) + "\n"
        return result

    def delete_data_base(self):
        self.db_connection.close()
        os.remove(self.name)

    def delete_student_table(self):
        self.db_cursor.execute(
            '''
            DROP TABLE Students;
            '''
        )
        self.save()

    def delete_all_tables(self):
        self.db_cursor.execute(
            '''
            DROP TABLE Students;
            '''
        )
        self.db_cursor.execute(
            '''
            DROP TABLE Teachers;
            '''
        )
        self.db_cursor.execute(
            '''
            DROP TABLE StudentGroups;
            '''
        )
        self.save()

    def __del__(self):
        try:
            self.save()
        except Exception as e:
            pass
        self.db_connection.close()
