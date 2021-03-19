load data local infile "food_data.csv"
into table food
fields terminated by ','
lines terminated by '\n'
ignore 1 lines;

-- load data local infile "comments.csv"
-- into table feedback
-- fields terminated by ','
-- lines terminated by '\n'
-- ignore 1 lines; 