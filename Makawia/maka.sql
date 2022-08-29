create database USERS;
use USERS;

drop table users;
create table users 
(ID int auto_increment, USER_NAME varchar(100) NOT NULL,PHONE_NO varchar(100),PS varchar(100),CPS varchar(100),primary KEY (ID));

select * from users;

