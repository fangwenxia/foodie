 -- Sample Data
   --  insert into diningHall (did, name, hours, waitTime)
   --  values (1, 'Bates', '7:30am to 7:30pm', 0);
   --  insert into diningHall (did, name, hours, waitTime)
   --  values (2, 'Lulu', '7am to 11pm', 5);
   --  insert into diningHall (did, name, hours, waitTime)
   --  values (3, 'Pom', '7:30am to 7:30pm', 2);
   --  insert into diningHall (did, name, hours, waitTime)
   --  values (4, 'Stone-D', '7:30am to 7:30pm', 10);
   --  insert into diningHall (did, name, hours, waitTime)
   --  values (5, 'Tower', '7:30am to 7:30pm', 15);

   --  insert into food (name, lastServed, type, did)
   --  values ('Taco Bowl', '2021-03-02', 'lunch', '2');

   --  insert into food (name, lastServed, type, did)
   --  values ('Egg Sandwich', '2021-03-02', 'breakfast', '5');

   --  insert into food (name, lastServed, type, did)
   --  values ('Beef Stroganoff', '2020-04-18', 'lunch', '5');
    
   --  insert into labels (allergen, preference, ingredients, fid)
   --  values ('wheat, milk', 'none', 'egg noodles', 3);

   --  insert into labels (allergen, preference, ingredients, fid)
   --  values ('eggs,milk,wheat', 'english muffin', 'none', 2);

   --  insert into labels (allergen, preference, ingredients, fid)
   --  values ('none', 'vegan', 'avocado', 1);

   --  insert into student(username, password, name, classYear, favoriteDH, favoriteFood)
   --  values ('sclark4','123','Sara Clark','2022', 2, 1);

   --  insert into student(username, password, name, classYear, favoriteDH, favoriteFood)
   --  values ('fx1','123','Fangwen Xia','2023',5, 3);

   --  insert into feedback(comment, rating, username, fid,entered)
   --  values ('Taco Tuesday at Lulu was great! The cilantro crema was weirdly sweet though.', 4, 'sclark4', 1,now());

   --  insert into feedback(comment, rating, username, fid,entered)
   --  values ('The croissant sandwich is ok, but I wish the fried eggs were not cooked so hard', 3, 'sclark4', 2,now());

-- insert into labels (allergen, preference, ingredients, fid)
--    values ('milk', 'none', 'mushroom, noodles', 10);
-- insert into labels (allergen, preference, ingredients, fid)
--    values ('wheat', 'none', 'apples', 11);
-- insert into labels (allergen, preference, ingredients, fid)
--    values ('wheat, eggs','eggs', 12);
-- insert into labels (allergen, preference, ingredients, fid)
--    values ('none', 'none', 'cucumber,rice', 13);
-- insert into labels (allergen, preference, ingredients, fid)
--    values ('milk', 'none', 'chicken,pasta,cheese', 14);
-- insert into labels (allergen, preference, ingredients, fid)
--    values ('milk', 'vegetarian', 'yogurt,strawberries', 15);
-- insert into labels (allergen, preference, ingredients, fid)
--    values ('eggs', 'vegetarian', 'egg,cream-cheese frosting', 16);
-- insert into labels (allergen, preference, ingredients, fid)
--    values ('soy', 'vegan', 'tofu,herbs', 17);
-- insert into labels (allergen, preference, ingredients, fid)
--    values ('fish', 'none', 'salmon,soy', 18);
-- insert into labels (allergen, preference, ingredients, fid)
--    values ('none', 'vegan', 'tomato,herbs', 19);
-- insert into labels (allergen, preference, ingredients, fid)
--    values ('eggs', 'vegetarian', 'eggs,chocolate', 20);

-- update food set type = 'all day' where fid = 12;
-- update food set type = 'all day' where fid = 16;
-- update food set type = 'all day' where fid = 20;

-- insert into food (name, lastServed, type, did)
--    values ('Pear', '2021-02-18', 'all day', '5');
-- insert into food (name, lastServed, type, did)
--    values ('Pear', '2021-02-18', 'all day', '5');
-- insert into labels (allergen, preference, ingredients, fid)
--    values ('wheat, milk', 'none', 'egg noodles', '3');
-- insert into food (fid,name,lastServed,type,did)
--       values ('4','Split Pea & Ham Soup', '2021-03-01','lunch','1')
-- insert into labels (allergen, preference, ingredients, fid)
--       values ('none', 'none', 'peas,ham', 4);
-- insert into food (fid,name,lastServed,type,did)
--       values ('5','Hawaiian Pizza', '2021-03-02','lunch','1')
-- insert into labels (allergen, preference, ingredients, fid)
--       values ('milk,wheat','none','pineapple,cheese,tomato', 5);
insert into food (fid,name,lastServed,type,did)
    values ('6','Chicken California Club', '2021-03-13','lunch','1');
insert into labels (allergen, preference, ingredients, fid)
      values ('milk,wheat', 'none', 'chicken','6');
insert into food (fid,name,lastServed,type,did)
    values ('7','Garlic Breadsticks', '2021-03-13','lunch','1');
insert into labels (allergen, preference, ingredients, fid)
      values ('milk,wheat,soy', 'vegetarian', 'flour,garlic,butter','7');
insert into food (fid,name,lastServed,type,did)
    values ('8','Broccoli and Cheddar Soup', '2021-03-15','lunch','1');
insert into labels (allergen, preference, ingredients, fid)
      values ('wheat,soy,milk', 'none', 'broccoli','8');
insert into food (fid,name,lastServed,type,did)
    values ('0','Roasted Butternut Squash', '2021-03-19','lunch','1');
insert into labels (allergen, preference, ingredients, fid)
      values ('soy', 'vegetarian', 'butternut squash','21');


