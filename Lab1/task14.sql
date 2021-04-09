-- Реализовать запросы с использованием аггрегатных функций:
-- a) определить суммарную стоимость всех заказов, произведенных потребителями из Канавинского района;
SELECT SUM(amount) FROM "Order", Customer
WHERE customer = Customer.ID
AND Customer.address = 'Канавинский';


-- b) найти среднее число заказываемых деталей с ценой более 2000;
SELECT AVG("Order".quantity) FROM "Order", Detail
WHERE detail = Detail.ID
AND Detail.price > 2000;


-- c) найти максимальную скидку среди потребителей, заказывавших детали у поставщиков из своего района;
SELECT MAX(discount) FROM "Order", Customer, Supplier
WHERE customer = Customer.ID AND supplier = Supplier.ID
AND customer.address = supplier.address;


-- d) какие детали имеют цену за штуку меньше средней.
SELECT DISTINCT Detail.ID, Detail.name FROM "Order", Detail
WHERE detail = Detail.ID
AND price < (SELECT AVG(price) FROM Detail);
