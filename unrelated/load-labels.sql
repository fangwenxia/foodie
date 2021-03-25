load data local infile "labels_data_updated.csv"
into table food
fields terminated by ','
lines terminated by '\n'
ignore 1 lines;
