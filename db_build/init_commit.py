from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey, text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from dotenv import dotenv_values
from urllib.parse import quote
from sqlalchemy.schema import CreateSchema

secrets = dotenv_values("../env/.env")
db_pwd = quote(secrets['DB_PASSWORD'])

# Database connection URI
DATABASE_URI = f"postgresql+psycopg2://{secrets['DB_USERNAME']}:{db_pwd}@localhost:5433/{secrets['DB_NAME']}"

# New SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Create schemas if they do not exist
with engine.connect() as conn:
    conn.execute(CreateSchema("equity", if_not_exists=True))
    conn.execute(CreateSchema("income", if_not_exists=True))
    conn.commit()

# Base class for declarative models
Base = declarative_base()

# Define tables
class Employer(Base):
    __tablename__ = 'employer'
    __table_args__ = {'schema': 'income'}
    id = Column(Integer, primary_key=True)
    employer_name = Column(String)
    employer_identification_number = Column(String)
    employer_control_number = Column(String)
    employer_state_id = Column(String)
    employer_address = Column(String)
    employer_address_cont = Column(String)
    employer_city = Column(String)
    employer_state = Column(String)
    employer_zip_code = Column(String)

class SelfEmployment(Base):
    __tablename__ = 'self_employment'
    __table_args__ = {'schema': 'income'}
    id = Column(Integer, primary_key=True)
    business_name = Column(String)
    business_identification_number = Column(String)
    business_address = Column(String)
    business_address_cont = Column(String)
    business_city = Column(String)
    business_state = Column(String)
    business_zip_code = Column(String)

class Paystub(Base):
    __tablename__ = 'paystub'
    __table_args__ = {'schema': 'income'}
    id = Column(Integer, primary_key=True)
    employer_self_employment_id = Column(Integer, ForeignKey('income.employer.id'))
    period_beginning = Column(Date)
    period_ending = Column(Date)
    pay_date = Column(Date)
    pay_rate = Column(Numeric)
    hours = Column(Numeric)
    bonus = Column(Numeric)
    commission = Column(Numeric)
    gross_pay = Column(Numeric)
    net_pay = Column(Numeric)
    deductions = Column(Numeric)
    gross_pay_ytd = Column(Numeric)
    net_pay_ytd = Column(Numeric)
    deductions_ytd = Column(Numeric)

class Deduction(Base):
    __tablename__ = 'deduction'
    __table_args__ = {'schema': 'income'}
    id = Column(Integer, primary_key=True)
    paystub_id = Column(Integer, ForeignKey('income.paystub.id'))
    federal_income_tax = Column(Numeric)
    social_security_tax = Column(Numeric)
    medicare_tax = Column(Numeric)
    state_income_tax = Column(Numeric)
    client_roth = Column(Numeric)
    client_401k = Column(Numeric)
    health_spending_account = Column(Numeric)
    medical = Column(Numeric)
    dental = Column(Numeric)
    vision = Column(Numeric)

class CarLoan(Base):
    __tablename__ = 'car_loan'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    lender_id = Column(Integer)
    lender_name = Column(String)
    billed_amount = Column(Numeric)
    interest_rate = Column(Numeric)
    term_length = Column(Integer)
    monthly_payment = Column(Numeric)
    additional_payments = Column(Numeric)
    remaining_amount = Column(Numeric)
    est_payoff_date = Column(Date)

class HomeLoan(Base):
    __tablename__ = 'home_loan'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    lender_id = Column(Integer)
    lender_name = Column(String)
    billed_amount = Column(Numeric)
    interest_rate = Column(Numeric)
    term_length = Column(Integer)
    monthly_payment = Column(Numeric)
    additional_payments = Column(Numeric)
    remaining_amount = Column(Numeric)
    est_payoff_date = Column(Date)

class PersonalLoan(Base):
    __tablename__ = 'personal_loan'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    lender_id = Column(Integer)
    lender_name = Column(String)
    billed_amount = Column(Numeric)
    interest_rate = Column(Numeric)
    term_length = Column(Integer)
    monthly_payment = Column(Numeric)
    additional_payments = Column(Numeric)
    remaining_amount = Column(Numeric)
    est_payoff_date = Column(Date)

class CreditLoan(Base):
    __tablename__ = 'credit_loan'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    lender_id = Column(Integer)
    lender_name = Column(String)
    billed_amount = Column(Numeric)
    interest_rate = Column(Numeric)
    monthly_payment = Column(Numeric)
    additional_payments = Column(Numeric)
    remaining_amount = Column(Numeric)

class RealEstateTax(Base):
    __tablename__ = 'real_estate_tax'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    entity = Column(String)
    item = Column(String)
    amount = Column(Numeric)
    date = Column(Date)
    due_date = Column(Date)

class PersonalPropertyTax(Base):
    __tablename__ = 'personal_property_tax'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    entity = Column(String)
    item = Column(String)
    amount = Column(Numeric)
    date = Column(Date)
    due_date = Column(Date)

class FederalTax(Base):
    __tablename__ = 'federal_tax'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    paystub_w2_id = Column(Integer, ForeignKey('income.paystub.id'))

class StateTax(Base):
    __tablename__ = 'state_tax'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    paystub_w2_id = Column(Integer, ForeignKey('income.paystub.id'))

class CapitalGainTax(Base):
    __tablename__ = 'capital_gain_tax'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    stock_bond_id = Column(Integer, ForeignKey('equity.stock.id'))

class Savings(Base):
    __tablename__ = 'savings'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    deposits = Column(Numeric)
    withdrawal = Column(Numeric)
    balance = Column(Numeric)
    margin = Column(Numeric)

class Stock(Base):
    __tablename__ = 'stock'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    deposits = Column(Numeric)
    withdrawal = Column(Numeric)
    balance = Column(Numeric)
    margin = Column(Numeric)

class Bond(Base):
    __tablename__ = 'bond'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    deposits = Column(Numeric)
    withdrawal = Column(Numeric)
    balance = Column(Numeric)
    margin = Column(Numeric)

class Retirement401k(Base):
    __tablename__ = 'retirement_401k'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    deposits = Column(Numeric)
    withdrawal = Column(Numeric)
    balance = Column(Numeric)
    margin = Column(Numeric)

class Roth(Base):
    __tablename__ = 'roth'
    __table_args__ = {'schema': 'equity'}
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    deposits = Column(Numeric)
    withdrawal = Column(Numeric)
    balance = Column(Numeric)
    margin = Column(Numeric)

# Create all tables with the .metadata.create_all() method
Base.metadata.create_all(engine)

## Creating a new session to interact with the database
# Session = sessionmaker(bind=engine)
# session = Session()

## Adding example data
# new_car_loan = CarLoan(
#     lender_id=1,
#     lender_name='Bank XYZ',
#     billed_amount=15000.00,
#     interest_rate=3.5,
#     term_length=60,
#     monthly_payment=300.00,
#     additional_payments=50.00,
#     remaining_amount=10000.00,
#     est_payoff_date='2026-05-20'
# )

## Add the record to the session and commit it to the database
# session.add(new_car_loan)
# session.commit()

## Close the session
# session.close()
