import random

from sqlalchemy.orm import sessionmaker


from models import Employee, engine, City

Session = sessionmaker(bind=engine)

# with Session() as session:
#     employee = Employee(
#         first_name="John",
#         last_name="Smith",
#         age=36
#     )
#     session.add(employee)
#     session.commit()

# with Session() as session:
#     employees = session.query(Employee).all()
#     for e in employees:
#         print(e.first_name, e.last_name, e.age)

# with Session() as session:
#     employees = session.query(Employee).filter_by(age=40)
#     for e in employees:
#         print(e.first_name, e.last_name, e.age)

# with Session() as session:
#     employees = session.query(Employee).filter(Employee.age >= 40)
#     for e in employees:
#         print(e.first_name, e.last_name, e.age)


# with Session() as session:
#     employees = session.query(Employee).where(Employee.age >= 40)
#     for e in employees:
#         print(e.first_name, e.last_name, e.age)

# with Session() as session:
#     employees = session.query(Employee).where(Employee.first_name.startswith("A"))
#     for e in employees:
#         print(e.first_name, e.last_name, e.age)

# with Session() as session:
#     employees = session.query(Employee).where(
#         (Employee.first_name.startswith("B") | (Employee.age > 50))
#     )
#     for e in employees:
#         print(e.first_name, e.last_name, e.age)

# with Session() as session:
#     employees = session.query(Employee).where(
#         (Employee.first_name.startswith("B") | (Employee.age > 50))
#     ).order_by(Employee.age.desc(), Employee.first_name)
#     for e in employees:
#         print(e.first_name, e.last_name, e.age)

# with Session() as session:
#     employee = session.query(Employee).first()
#     print(employee.first_name, employee.last_name, employee.age)
#     employee.first_name = "Ivan"
#     session.commit()

# with Session() as session:
#     session.add_all((
#         City(name= "Varna"),
#         City(name= "Sofia"),
#         City(name= "Plovdiv"),
#         City(name= "Pleven"),
#         City(name= "Bourgas")
#     ))
#     session.commit()

# with Session() as session:
#     employees = session.query(Employee).all()
#     for e in employees:
#         e.city_id = random.randint(1, 5)
#     session.commit()

# with Session() as session:
#     city = session.query(City).first()
#     for e in city.employees:
#         print(e.first_name, e.last_name, city.name)
