drop table if exists admin;

use foodie_db;

create table admin (
    adminname varchar(15) not null,
    primary key (adminname),
    foreign key (adminname) references student(username)
        on update restrict
        on delete restrict
) 
ENGINE = InnoDB; 

-- insert into admin(adminname) values ('lteffera'); 
-- insert into admin(adminname) values ('sclark4'); 
-- insert into admin(adminname) values ('ggabeau'); 
-- insert into admin(adminname) values ('fx1'); 
-- insert into admin(adminname) values ('scott'); 