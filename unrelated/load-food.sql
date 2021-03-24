load data local infile "food_data_updated.csv"
into table food
fields terminated by ','
lines terminated by '\n'
ignore 1 lines;

