-- Используя операцию EXISTS ( NOT EXISTS ) реализовать нижеследующие запросы. 
-- В случае, если для текущего состояния БД запрос будет выдавать пустое множество строк, 
-- требуется указать какие добавления в БД необходимо провести.
-- a) определить потребителей, заказывавших детали с ценой более 6000руб.
-- у всех поставщиков из Советского или Канавинского районов;
SELECT Customer.ID, Customer.name FROM "Order", Customer, Supplier, Detail
WHERE customer = Customer.ID AND supplier = Supplier.ID AND detail = Detail.ID
AND EXISTS (SELECT price FROM Detail
	 	    WHERE price > 6000)
AND Supplier.address IN ('Советский', 'Канавинский');

-- INSERT INTO Detail (ID, name, storage, quantity, price) VALUES (008, 'Гайка', 'Сормовский', 20000, 7000);
-- INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (000018, 'Январь',  002, 003, 008, 5, 35000);

SELECT Customer.ID, Customer.name FROM "Order", Customer, Supplier, Detail
WHERE customer = Customer.ID AND supplier = Supplier.ID AND detail = Detail.ID
AND price > 6000
AND Supplier.address IN ('Советский', 'Канавинский');


-- b) найти деталь, которую заказывали в количестве одной штуки все потребители;
SELECT Detail.ID, Detail.name FROM Detail
WHERE EXISTS (SELECT * FROM (SELECT COUNT (customer)
			   FROM (SELECT DISTINCT customer
	  				 FROM "Order"
	  				 WHERE quantity = 1)
			   AS DistinctCustomers) AS Counter
			  WHERE Counter.count = 5);
			  
-- INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00019, 'Январь',  001, 004, 003, 1, 25000);
-- INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00020, 'Февраль',  002, 003, 003, 1, 1000);
-- INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00021, 'Апрель',  003, 002, 003, 1, 3000);
-- INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00022, 'Март',  005, 001, 003, 1, 1500);


SELECT DISTINCT Detail.name FROM "Order", Detail
WHERE detail = Detail.ID
AND "Order".quantity = 1;


-- c) какие детали не заказывали потребители с размером скидки менее 5%;
SELECT * FROM "Order"
WHERE NOT EXISTS
(SELECT DISTINCT detail FROM "Order"
 WHERE detail NOT IN (SELECT DISTINCT detail FROM "Order"
					  WHERE customer IN (SELECT ID FROM Customer
				  						 WHERE discount < 5)));

-- Предыдущие запрос вернул пустую таблицу, значит есть такие детали, которые не заказывали потребители,
-- имеющие скидку меньше 5%. Найдем их:

SELECT DISTINCT Detail.ID, Detail.name FROM "Order", Detail
WHERE detail = Detail.ID 
AND detail IN 
(SELECT DISTINCT detail FROM "Order"
 WHERE detail NOT IN (SELECT DISTINCT detail FROM "Order"
					  WHERE customer IN (SELECT ID FROM Customer
				  						 WHERE discount < 5)));


-- d) найти потребителя, заказывавшего все детали, не поставляемые поставщиками из Сормовского района.
-- INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00023, 'Январь',  002, 004, 004, 5, 45000);
-- Аналогичные запросы можно сделать для кажого потребителя (Customer = 1, 3, 4, 5)
SELECT DISTINCT Customer.ID, Customer.name FROM "Order", Customer
WHERE customer = Customer.ID
AND NOT EXISTS (
	(SELECT DISTINCT detail
	 FROM "Order"
	 WHERE detail NOT IN (SELECT DISTINCT detail
					 	  FROM "Order", Supplier
					 	  WHERE supplier = Supplier.ID
					  	  AND Supplier.address = 'Сормовский'))
	EXCEPT
	(SELECT DISTINCT detail
	 FROM "Order"
	 WHERE customer = 2))
AND customer = 2;
	 
