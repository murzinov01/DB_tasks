-- Вывести:
-- a) названия и размер скидки организаций-потребителей, куда поставлял детали Щепин,
-- а общая сумма заказа превышала 5000;
SELECT Customer.name, discount FROM "Order", Customer, Supplier
WHERE customer = Customer.ID AND supplier = Supplier.ID AND supplier.surname = 'Щепин' AND amount > 5000;


-- b) фамилии и размер комиссионных для поставщиков, поставлявших детали предприятиям чужих районов
-- не ранее января. Отсортировать по возрастанию комиссионных; 
SELECT surname, commission FROM "Order", Customer, Supplier
WHERE customer = Customer.ID AND supplier = Supplier.ID
AND supplier.address != customer.address AND date NOT IN ('Январь', 'Февраль')
ORDER BY commission ASC;


-- c) название и оставшееся количество деталей, заказывавшихся в количестве более 2 штук
-- предприятиями Автозаводского и Советского районов. В вывод добавить суммарную стоимость соответствующих заказов;
SELECT Detail.name, Detail.quantity - "Order".quantity as "remaining number of details", amount FROM "Order", Customer, Supplier, Detail
WHERE customer = Customer.ID AND supplier = Supplier.ID AND detail = Detail.ID
AND (customer.address = 'Автозаводский' OR customer.address = 'Советский')
AND detail > 2;


-- d) названия предприятий одного района, заказывавших молотки.
SELECT Customer.name FROM "Order", Customer
WHERE customer = Customer.ID AND Customer.address IN 
		(SELECT Customer.address FROM "Order", Customer, Detail
		 WHERE customer = Customer.ID AND detail = Detail.ID
		 AND Detail.name = 'Молоток'
		 GROUP BY Customer.address
		 HAVING COUNT(Customer.address) > 1);
