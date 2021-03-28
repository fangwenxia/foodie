load data local infile "comments_data_updated_2.csv"
into table feedback
fields terminated by ','
lines terminated by '\n'
ignore 2 lines; 
insert into student(username, name, favoriteDH, favoriteFood)
    values ('lteffera','Leah Teffera',1, 1001) --ONLY RUN ONCE!! 
