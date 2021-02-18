#!/usr/bin/python3

# See http://docs.sqlalchemy.org/en/rel_1_1/orm/tutorial.html
# for a great tutorial on getting started with the SqlAlchemy ORM.

import getpass
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import or_, and_, text, func

secret = getpass.getpass('Enter password: ')

engine = create_engine('postgresql+pg8000://cpainter:' + secret + '@flowers.mines.edu/csci403', echo=True)

Base = declarative_base()

# Define a class describing a database table
class Person(Base):
    __tablename__ = 'sqa_person'
    id = Column(Integer, primary_key=True)
    lastname = Column(String)
    firstname = Column(String)
    emails = relationship("Email", back_populates="person")
    def __repr__(self):
        return "<Person ('%s, %s')>" % (self.lastname, self.firstname)

class Email(Base):
    __tablename__ = 'sqa_email'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey('sqa_person.id'))
    person = relationship("Person", back_populates="emails")
    def __repr__(self):
        return "<Email ('%s')>" % self.address

# Create table(s) (unless already existing) 
Base.metadata.create_all(engine)

alice = Person(lastname = 'Appleby', firstname = 'Alice')
print(alice)

Session = sessionmaker(bind=engine)
session = Session()

session.add(alice)

session.add_all([
    Person(firstname = 'Bob', lastname = 'Bartlett'),
    Person(firstname = 'Carol', lastname = 'Custer'),
    Person(firstname = 'Doug', lastname = 'Douglass')])

alice.lastname = 'Smith'

alice.emails = [
    Email(address = 'alice@google.com'),
    Email(address = 'aappleby@mymail.mines.edu')]

#session.dirty

#session.new

session.commit()

session.query(Person).all()

#session.query(Person).filter(Person.firstname != 'Alice').all()

#session.query(Person).filter_by(firstname = 'Alice').all()

#session.query(Person).filter(Person.firstname.in_(['Bob','Carol'])).all()

#session.query(Person).filter(Person.firstname.like('B%')).all()

#for instance in session.query(Person).order_by(Person.lastname):
    #print(instance.firstname, instance.lastname)

#session.query(Person.lastname).all()

#session.query(Person).filter(Person.firstname.in_(
#    session.query(Person.firstname).filter(Person.firstname.like('C%')))).all()

#session.query(Person).filter(Person.firstname != None).all()

#session.query(Person).filter(or_(Person.firstname = 'Bob', Person.lastname = 'Smith', Person.lastname = 'Custer')).all()

#session.query(Person).from_statement(
    #text("SELECT * FROM sqa_person WHERE firstname='Bob'")).all()

#session.query(func.count(Person.firstname), Person.firstname).group_by(Person.firstname).all()

someone = session.query(Person).filter(Person.firstname == 'Alice').one()

print(someone)

print(someone.emails)

someone = session.query(Person).filter(Person.firstname == 'Bob').one()
print(someone)

session.delete(someone)
session.query(Person).filter(Person.firstname == 'Bob').count()


