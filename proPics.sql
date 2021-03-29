drop table if exists proPics;
create table proPics(
    --  username varchar(15), -- user posting photo
     username varchar(225), -- id of food photo is associated with
     filename varchar(50), --
     primary key (username),
    --  foreign key (username) references student(username)
    --     on update cascade
    --     on delete cascade,
    foreign key (username) references student(username)
        on update cascade
        on delete cascade
    )
    ENGINE = InnoDB;