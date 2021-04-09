-- Используя операцию IN (NOT IN) реализовать следующие запросы:
-- a) найти всех потребителей, заказывавших болты или винты не менее двух раз;
SELECT Customer.name FROM Customer WHERE Customer.ID IN
(SELECT customer FROM "Order", Customer, Detail
WHERE "Order".customer = Customer.ID AND "Order".detail = Detail.ID
AND Detail.name IN ('Болт', 'Винт')
GROUP BY customer
HAVING COUNT (customer) > 1); 


-- b) найти потребителей, не делавших заказов на сумму менее 500000руб. поставщикам из своего района
SELECT * FROM "Order", Customer, Supplier
WHERE "Order".customer = Customer.ID AND "Order".supplier = Supplier.ID
AND Customer.address IN (Supplier.address) AND amount > 500000;


-- c) запросы задания 7.с и 7.d.
SELECT Detail.name, Detail.quantity - "Order".quantity as "remaining number of details", amount FROM "Order", Customer, Supplier, Detail
WHERE customer = Customer.ID AND supplier = Supplier.ID AND detail = Detail.ID
AND customer.address IN ('Автозаводский', 'Советский')
AND detail > 2;
 
SELECT Customer.name FROM "Order", Customer
WHERE customer = Customer.ID AND Customer.address IN 
		(SELECT Customer.address FROM "Order", Customer, Detail
		 WHERE customer = Customer.ID AND detail = Detail.ID
		 AND Detail.name = 'Молоток'
		 GROUP BY Customer.address
		 HAVING COUNT(Customer.address) > 1);