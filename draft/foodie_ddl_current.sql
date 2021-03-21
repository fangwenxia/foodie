-- Sara Clark, Fangwen Xia, Leah Teffera, Gigi Gabeau
use foodie_db;
drop table if exists labels;
drop table if exists feedback;
drop table if exists student;
drop table if exists food;
drop table if exists diningHall;
-- CHANGES:
-- need to be able to search menu by current location of a food item, potential solution: 
-- have variable for last served time and location
-- adding datetime in feedback table

create table diningHall(
     did int not null, -- dining hall id
     name varchar(30),
     hours varchar(40),
     waitTime int,
     primary key (did)
    )
    ENGINE = InnoDB;

create table food(
     fid int not null auto_increment, -- food id
     name varchar(50), -- some of the food titles from WellesleyFresh are really long
     lastServed date,
     type set('breakfast', 'lunch', 'dinner', 'all day'),
     did int,
     primary key (fid),
     foreign key (did) references diningHall(did)
        on update restrict
        on delete restrict
        )
    ENGINE = InnoDB;

create table student(
    username varchar(15) not null,
    password varchar(30),
    name varchar(30),
    classYear enum('2021','2022','2023','2024','Davis Scholar'),
    favoriteDH int,
    favoriteFood int,
    primary key (username),
    foreign key (favoriteDH) references diningHall(did)
        on delete restrict
        on update restrict,
    foreign key (favoriteFood) references food(fid)
        on delete restrict
        on update restrict
) 
    ENGINE = InnoDB; 

create table feedback(
     comment varchar(280),
     rating int,-- rating from 1 to 5, 5 being would recommend and 1 being would not recommend
     username varchar(15), -- user giving feedback
     fid int, -- id of food being critiqued
     entered datetime,
     primary key (username, fid),
     foreign key (username) references student(username)
        on update restrict
        on delete restrict
    foreign key (fid) references food(fid)
       on update restrict
       on delete restrict
    )
    ENGINE = InnoDB;

create table labels( 
    lid int not null auto_increment, -- label id
    -- from wellesley fresh website
    allergen set('none','eggs', 'fish', 'milk', 'peanuts', 'shellfish', 'soy', 'tree nut', 'wheat'),
    preference set('none','gluten sensitive', 'vegan', 'vegetarian', 'kosher', 'halal'),
    ingredients varchar(80),
    fid int,
    primary key (lid),
    foreign key (fid) references food(fid)
        on update restrict
        on delete restrict)
    ENGINE = InnoDB;