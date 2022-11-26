DROP TABLE IF EXISTS Address CASCADE;
DROP TABLE IF EXISTS Branch CASCADE;
DROP TABLE IF EXISTS Customer CASCADE;
DROP TABLE IF EXISTS Account CASCADE;
DROP TABLE IF EXISTS Employee CASCADE;
DROP TABLE IF EXISTS Transactions CASCADE;
DROP TABLE IF EXISTS to_from CASCADE;


Create table Address(
	Address_Id varchar(10) primary key,
	City varchar(20),
	State varchar(20),
	Zip char(5)
	--include check for address_id
	);

Create table Branch(
	Branch_Id varchar(10) primary key,
 	Status varchar(8),
	Address_Id varchar(10) references Address
	--include check for status and branch_Id
	check(Status='Active' or Status='Closed')
	);

Create table Customer(
	Customer_Id varchar(10) primary key,
	Name varchar(30),
	Branch_Id varchar(10) references Branch,
	Address_Id varchar(10) references Address
	--include check for Customer Id
	);

Create table Account(
	Account_Id varchar(10) primary key,
	Type varchar(2),
	Balance numeric(13,3),
	Customer_Id varchar(10) references Customer
	--include check statement for Type and balance
	check(balance>0),
	check(type='C' or type='S')
	);

Create table Employee(
	Employee_Id varchar(10) primary key,
	Name varchar(30),
	Position varchar(20),
	SSN char(9),
	Salary numeric(10,2),
	Address_Id varchar(10) references Address,
	Branch_Id varchar(10) references Branch
	--include check for employee id, ssn
	);

Create table Transactions(
	Transaction_Id varchar(10) primary key,
	Type varchar(20),
	Amount numeric(13,3),
	Description varchar(30),
	Customer_Id varchar(10) references Customer,
	Employee_Id varchar(10) references Employee
	--include check for amount and customer,employee
	check(Type='Deposit' or Type='Withdrawl' or Type='Transfer')
	);

Create table to_from(
	Transaction_Id varchar(10) references Transactions,
	From_account varchar(10) references Account(Account_Id),
	To_account varchar(10) references Account(Account_Id),
	primary key (Transaction_Id,From_account,To_account)
	);
