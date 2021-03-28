drop table if exists foodPics;
create table foodPics(
    --  username varchar(15), -- user posting photo
     fid int, -- id of food photo is associated with
     filename varchar(50), --
     primary key (fid),
    --  foreign key (username) references student(username)
    --     on update cascade
    --     on delete cascade,
    foreign key (fid) references food(fid)
        on update cascade
        on delete cascade
    )
    ENGINE = InnoDB;