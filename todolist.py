from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def user_input():
    print("""1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit""")
    return int(input('> '))


def day_task(day=str(datetime.today().day) + ' ' + str(datetime.today().strftime('%b'))):
    print('Today ' + day + ':')
    session = Session()
    tasks = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    if not tasks:
        print('Nothing to do!\n')
    else:
        counter = 0
        for row in tasks:
            counter += 1
            print(str(counter) + '. ' + row.task)
        print('')
    session.commit()


def add_task():
    session = Session()
    tsk = input('Enter task: ')
    dln = input('Enter deadline: ').split('-')
    new_row = Table(task=tsk, deadline=datetime(int(dln[0]), int(dln[1]), int(dln[2])))
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')


def all_tasks():
    print('All tasks:')
    session = Session()
    tasks = session.query(Table).order_by(Table.deadline).all()
    counter = 0
    for row in tasks:
        counter += 1
        dln = f'{row.deadline.day} {row.deadline:%b}'
        print(str(counter) + '. ' + row.task + '. ' + dln)
    print('')
    session.commit()


def week_tasks():
    day = datetime.today()
    for i in range(7):
        print(f'{day:%A} {day.day} {day:%b}:')
        session = Session()
        tasks = session.query(Table).filter(Table.deadline == day.date()).all()
        if not tasks:
            print('Nothing to do!\n')
        else:
            counter = 0
            for row in tasks:
                counter += 1
                print(str(counter) + '. ' + row.task)
            print('')
        session.commit()
        day += timedelta(days=1)


def missed_tasks():
    session = Session()
    tasks = session.query(Table).filter(Table.deadline < datetime.today()).all()
    if not tasks:
        print('Nothing is missed!')
    else:
        counter = 0
        for row in tasks:
            counter += 1
            print(f'{counter}. {row.task}. {row.deadline.day} {row.deadline:%b}')
    print("")
    session.commit()


def delete_task():
    print("Choose the number of the task you want to delete:")
    session = Session()
    tasks = session.query(Table).order_by(Table.deadline).all()
    counter = 0
    for row in tasks:
        counter += 1
        dln = f'{row.deadline.day} {row.deadline:%b}'
        print(str(counter) + '. ' + row.task + '. ' + dln)
    to_delete = int(input(">"))
    specific_task = tasks[to_delete - 1]
    session.delete(specific_task)
    session.commit()
    print("The task has been deleted!")


while (menu := user_input()) != 0:
    print('')
    if menu == 1:  # Today's tasks
        day_task()
    elif menu == 2:  # Week's tasks
        week_tasks()
    elif menu == 3:  # All tasks
        all_tasks()
    elif menu == 4:  # Missed tasks
        missed_tasks()
    elif menu == 5:  # Add task
        add_task()
    elif menu == 6:  # Delete task
        delete_task()
print('Bye!')