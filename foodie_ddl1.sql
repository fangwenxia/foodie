-- Sara Clark, Fangwen Xia, Leah Teffera, Gigi Gabeau
drop table if exists labels;
drop table if exists feedback;
drop table if exists student;
drop table if exists food;
drop table if exists DHstaff;
drop table if exists diningHall;

use foodie_db;

create table diningHall(
     did int not null, -- dining hall id
     name varchar(30),
     hours varchar(40),
     waitTime int,
     primary key (did)
    )
    ENGINE = InnoDB;

create table DHstaff ( -- dining hall staff
    sid int not null, -- staff id
    name varchar(30),
    worksAt int not null, -- id of dining hall
    primary key (sid),
    foreign key (worksAt) references diningHall(did)
        on update restrict
        on delete restrict)
ENGINE = InnoDB;

create table food(
     fid int not null, -- food id
     name varchar(30),
     lastServed date,
     type set('breakfast', 'lunch', 'dinner', 'all day'),
     did int,
     primary key (fid),
     foreign key (did) references diningHall(did)
        on update restrict
        on delete restrict
        )
    ENGINE = InnoDB;

create table student (
    username varchar(15) not null,
    name varchar(30),
    favoriteDH int,
    favoriteFood int,
    primary key (username),
    foreign key (favoriteDH) references diningHall(did)
        on update restrict
        on delete restrict,
    foreign key (favoriteFood) references food(fid)
        on update restrict
        on delete restrict
) 
ENGINE = InnoDB; 

create table feedback(
     comment varchar(280),
     rating int,-- rating from 1 to 5, 5 being would recommend and 1 being would not recommend
     username varchar(15), -- user giving feedback
     fid int, -- id of food being critiqued
     index(comment),
     primary key (username, fid),
     foreign key (username) references student(username)
        on update restrict
        on delete restrict,
    foreign key (fid) references food(fid)
        on update restrict
        on delete restrict
    )
    ENGINE = InnoDB;

create table labels(
    lid int not null, -- label id
    -- from wellesley fresh website
    allergen set('eggs', 'fish', 'milk', 'peanuts', 'shellfish', 'soy', 'tree nut', 'wheat'),
    preference set('gluten sensitive', 'vegan', 'vegetarian', 'kosher', 'halal'),
    ingredients varchar(80),
    fid int,
    primary key (lid),
    foreign key (fid) references food(fid)
        on update restrict
        on delete restrict)
    ENGINE = InnoDB;

    -- Sample Data
    insert into diningHall (did, name, hours, waitTime)
    values (1, 'Bates', '7:30am to 7:30pm', 0);
    insert into diningHall (did, name, hours, waitTime)
    values (2, 'Lulu', '7am to 11pm', 5);
    insert into diningHall (did, name, hours, waitTime)
    values (3, 'Pom', '7:30am to 7:30pm', 2);
    insert into diningHall (did, name, hours, waitTime)
    values (4, 'Stone-D', '7:30am to 7:30pm', 10);
    insert into diningHall (did, name, hours, waitTime)
    values (5, 'Tower', '7:30am to 7:30pm', 15);

    insert into DHstaff (sid, name, worksAt)
    values (1, 'Tim', 1);

    insert into food (fid, name, lastServed, type, did)
    values (1, 'Taco Bowl', '2021-03-02', 'lunch', '2');

    insert into food (fid, name, lastServed, type, did)
    values (2, 'Egg Sandwich', '2021-03-02', 'breakfast', '5');

    insert into labels (lid, allergen, ingredients, fid)
    values (1, 'eggs,milk,wheat', 'english muffin, fried egg', 2);

    insert into labels (lid, preference, ingredients, fid)
    values (2, 'vegan', 'avocado', 1);

    insert into student(username, name, favoriteDH, favoriteFood)
    values ('sclark4', 'Sara Clark', 2, 1);

    insert into feedback(comment, rating, username, fid)
    values ('Taco Tuesday at Lulu was great! The cilantro crema was weirdly sweet though.', 4, 'sclark4', 1);

    insert into feedback(comment, rating, username, fid)
    values ('The croissant sandwich is ok, but I wish the fried eggs were not cooked so hard', 3, 'sclark4', 2);