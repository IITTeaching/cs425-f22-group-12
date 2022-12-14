DROP TABLE IF EXISTS Address CASCADE;
DROP TABLE IF EXISTS Branch CASCADE;
DROP TABLE IF EXISTS Customer CASCADE;
DROP TABLE IF EXISTS Account CASCADE;
DROP TABLE IF EXISTS Employee CASCADE;
DROP TABLE IF EXISTS Transactions CASCADE;
DROP TABLE IF EXISTS to_from CASCADE;
DROP TABLE IF EXISTS to_from_ext CASCADE;


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
	Address_Id varchar(10) references Address,
	--include check for Customer Id
	Password varchar(10)
	);

Create table Account(
	Account_Id varchar(10) primary key,
	Type varchar(2),
	Balance numeric(13,3),
	Customer_Id varchar(10) references Customer,
	status varchar(10),
	check(status='Active' or Status='Closed'),
	--include check statement for Type and balance
	check(type='C' or type='S')
	);

Create table Employee(
	Employee_Id varchar(10) primary key,
	Name varchar(30),
	Position varchar(20),
	SSN char(9),
	Salary numeric(10,2),
	Address_Id varchar(10) references Address,
	Branch_Id varchar(10) references Branch,
	Password varchar(10)
	--include check for employee id, ssn
	check(Position='Manager' or Position='Teller')

	);

Create table Transactions(
	Transaction_Id varchar(10) primary key,
	Type varchar(20),
	Amount numeric(13,3),
	Description varchar(30),
	Customer_Id varchar(10),
	Employee_Id varchar(10),
	CurrBalance_from numeric(13,3),
	CurrBalance_to numeric(13,3) default NULL,
	day date default current_timestamp,
	--include check for amount and customer,employee
	check(Type='Deposit' or Type='Withdrawl' or Type='Transfer' or Type='ExtTransfer')
	);

Create table to_from(
	Transaction_Id varchar(10) references Transactions,
	From_account varchar(10) references Account(Account_Id),
	To_account varchar(10) references Account(Account_Id),
	primary key (Transaction_Id,From_account,To_account)
	);

Create table to_from_ext(
	Transaction_Id varchar(10) references Transactions,
	From_account varchar(10) references Account(Account_Id),
	To_bank varchar(30),
	Account_number VARCHAR(12),
	Routing_number varchar(9),
	primary key (Transaction_Id,From_account,To_bank, Account_number, Routing_number)
	);
