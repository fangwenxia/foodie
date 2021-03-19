load data local infile "food_data.csv"
into table food
fields terminated by ','
lines terminated by '\n'
ignore 1 lines;

