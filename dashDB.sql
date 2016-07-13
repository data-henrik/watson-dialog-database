-- SQL statements to create the table "dialogdata" and insert few rows
drop table dialogdata;
create table dialogdata(cid int unique not null, fname varchar(50),lname varchar(50),
bdate date);

insert into dialogdata values
(10,'Henrik','Sample','1990-05-11'),
(20,'John','Doe','1980-02-13'),
(30,'Max','Mustermann','1977-09-22');
