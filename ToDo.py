from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

rows = session.query(Table).all()


def p_menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")


weekname = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
            4: "Friday", 5: "Saturday", 6: "Sunday"}
today = datetime.today()

p_menu()
while True:
    x = int(input())
    if x == 1:
        form_date = str(datetime.today().__format__('%Y-%m-%d'))
        emp = 0
        print(f"Today {today.day} {today.strftime('%b')}:")
        num_task = 0
        for i in rows:
            if str(i.deadline) == form_date:
                emp = 1
                num_task += 1
                print(f"{num_task}. {i}")

        if emp == 0:
            print("Nothing to do!")
        else:
            emp = 0
        print()
        p_menu()

    elif x == 2:
        for z in range(7):
            emp = 0
            dayz = today + timedelta(days=z)
            form_date = str(dayz.__format__('%Y-%m-%d'))
            print(f"{weekname[dayz.weekday()]} {dayz.day} {dayz.strftime('%b')}:")
            num_task = 0
            for i in rows:
                if str(i.deadline) == form_date:
                    emp = 1
                    num_task += 1
                    print(f"{num_task}. {i}")
            if emp == 0:
                print("Nothing to do!")
            else:
                emp = 0
            print()
        p_menu()
    elif x == 3:
        rows = session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        num_task = 0
        for i in rows:
            num_task += 1
            print(f"{num_task}. {i}. {i.deadline.day} {i.deadline.strftime('%b')}")
        print()
        p_menu()
    elif x == 0:
        print()
        print("Bye!")
        break
    elif x == 4:
        rows = session.query(Table).order_by(Table.deadline). \
            filter(Table.deadline < datetime.today().date()).all()
        num_task = 0
        if len(rows) == 0:
            print("Nothing is missed!")
        else:
            for i in rows:
                num_task += 1
                print(f"Missed tasks: \n{num_task}. {i} {i.deadline.day} {i.deadline.strftime('%b')}")
        print()
        p_menu()
    elif x == 5:
        print()
        print("Enter task")
        new_task = input()
        print("Enter deadline")
        new_dead = input()
        form_dead = datetime.strptime(new_dead, '%Y-%m-%d').date()
        new_row = Table(task=new_task,
                        deadline=form_dead)
        session.add(new_row)
        session.commit()
        rows = session.query(Table).all()
        print("The task has been added!")
        print()
        p_menu()
    elif x == 6:
        rows = session.query(Table).order_by(Table.deadline).all()
        if len(rows) == 0:
            print("Nothing to delete")
        else:
            dict_num_task = {}
            dict_date = {}
            print("Choose the number of the task you want to delete:")
            num_task = 0
            for i in rows:
                num_task += 1
                dict_num_task.setdefault(num_task, i)
                dict_date.setdefault(i, i.deadline)
                print(f"{num_task}. {i} {i.deadline.day} {i.deadline.strftime('%b')}")
            task_del = dict_num_task[int(input())]
            date_del = dict_date[task_del]
            session.query(Table).filter(Table.deadline == date_del and Table.task == task_del).delete()
            session.commit()
            print("The task has been deleted!")
        print()
        p_menu()