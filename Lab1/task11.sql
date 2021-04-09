-- Используя операции ALL-ANY реализовать следующие запросы:
-- a) найти поставщика с наименьшими комиссионными, который в мае 
-- поставлял детали потребителю, сделавшему заказ максимальной стоимости в апреле;
SELECT Supplier.ID, Supplier.surname FROM "Order", Supplier
WHERE supplier = Supplier.ID
AND customer = (SELECT customer FROM "Order", Customer
				WHERE customer = Customer.ID
			   	AND date = 'Апрель'
			    AND amount >= ALL (SELECT amount FROM "Order"
								   WHERE date = 'Апрель'))
AND customer IN 
(SELECT customer FROM "Order", Supplier
WHERE supplier = Supplier.ID
AND date = 'Май' AND commission <= ALL (SELECT commission FROM "Order", Supplier
									   WHERE supplier = Supplier.ID AND date = 'Май'));


-- b) найти деталь у которой цена совпадает с ценой какой-либо ( но не той же самой) детали,
-- проданной поставщиком из Советского района с максимальными комиссионными;																													
SELECT Detail.ID, Detail.name FROM "Order", Detail, (SELECT DISTINCT Detail.ID, Detail.price FROM "Order", Detail
 								WHERE detail = Detail.ID
  								AND supplier = (SELECT ID FROM Supplier
  										 		WHERE address = 'Советский'
  										 		AND commission >= ALL (SELECT commission FROM Supplier
 																	   WHERE address = 'Советский'))) AS TargetDetails
WHERE detail = Detail.ID
AND Detail.ID != TargetDetails.ID
AND Detail.price = TargetDetails.price;


-- c) найти потребителя, который имеет не максимальный размер скидки и покупал детали у поставщиков из Канавинского района;
SELECT Customer.ID, Customer.name FROM "Order", Customer, Supplier
WHERE customer = Customer.ID AND supplier = Supplier.ID
AND Supplier.address = 'Канавинский'
AND Customer.discount != (SELECT discount FROM Customer
						  WHERE discount >= ALL (SELECT discount FROM Customer));


-- d) запрос задания 7.а.
SELECT Customer.name, discount FROM "Order", Customer, Supplier
WHERE customer = Customer.ID AND supplier = Supplier.ID
AND supplier.surname = 'Щепин'
AND amount = ANY (SELECT amount FROM "Order"
				  WHERE amount > 5000);