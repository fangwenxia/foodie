load data local infile "comments_data_updated.csv"
into table feedback
fields terminated by ','
lines terminated by '\n'
ignore 1 lines; 