-- Creating initial adresses
INSERT INTO Address VALUES('ADDB7F8224', 'Chicago', 'IL', '60653');
INSERT INTO Address VALUES('AD9A4687AC', 'Chicago', 'IL', '60639');

-- Creating initial branches
INSERT INTO Branch VALUES('BR44122B41', 'Active', 'ADDB7F8224');
INSERT INTO Branch VALUES('BRE37AB30F', 'Active', 'AD9A4687AC');

-- Creating employees
INSERT INTO employee VALUES('EMD76A86FC', 'Achraf Kamni', 'Manager', '509204145', 150000.00, 'ADDB7F8224', 'BR44122B41');
INSERT INTO employee VALUES('EMBE09F2D2', 'Sasidharan Nair Darshan', 'Teller', '247881067', 50000.00, 'AD9A4687AC', 'BRE37AB30F');