drop table if exists proPics;
create table proPics(
     username varchar(225), -- username of person whose profile picture it belongs to
     filename varchar(50),
     primary key (username),
    foreign key (username) references student(username)
        on update cascade
        on delete cascade
    )
    ENGINE = InnoDB;