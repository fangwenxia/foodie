-- SQL statements to copy the WMDB tables into tables in the current
-- database.  Note that there is no "use" statement in this script, so if
-- you start the mysql client, "use" your own database, then source this
-- file, you will get copies of the most important WMDB tables in your
-- current database.

-- Don't source this script while in the WMDB.  It won't work (hopefully).

drop table if exists credit;
drop table if exists movie;
drop table if exists picfile;
drop table if exists picblob;
drop table if exists person;
drop table if exists staff;

create table staff like wmdb.staff;
insert into staff
select * from wmdb.staff;

create table person like wmdb.person;
insert into person
select * from wmdb.person;

create table movie like wmdb.movie;
insert into movie
select * from wmdb.movie;

create table credit like wmdb.credit;
insert into credit
select * from wmdb.credit;
