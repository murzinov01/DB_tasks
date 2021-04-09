-- Используя средства группировки реализовать следующие запросы:
-- a) найти для каждой пары “потребитель-поставщик” суммарную величину стоимости произведенных заказов;
SELECT Customer.name, Supplier.surname,
SUM(amount) as total_amount
FROM "Order", Customer, Supplier
WHERE customer = Customer.ID AND supplier = Supplier.ID
GROUP BY Customer.name, Supplier.surname
ORDER BY total_amount ASC;


-- b) найти детали, которые более трех раз заказывали потребители из Советского района;
SELECT Detail.ID, Detail.name FROM Detail
WHERE id IN 
(SELECT DISTINCT detail
 FROM 
 (SELECT Customer.address, detail,
  COUNT(*) as total_orders
  FROM "Order", Customer
  WHERE customer = Customer.ID
  GROUP BY Customer.address, detail
  ORDER BY total_orders ASC)
 AS Detail_groups
 WHERE total_orders > 3);
 

-- c) найти месяц, в котором все заказы имели стоимость не менее 10000;
SELECT date,
SUM(amount) as total_amount
FROM "Order"
GROUP BY date
ORDER BY total_amount ASC;


-- d) получить для каждой детали с ценой более 10000 среднее количество заказываемых деталей.
-- Деталей с ценой больше 10000 у нас нет, поэтому мы сделали это задание для деталей с ценой больше 1000
Select New_details.name,
AVG("Order".quantity) as avg_quantity
FROM "Order",
(SELECT * FROM Detail
 WHERE price > 1000) 
 AS New_details
WHERE detail = New_details.ID
GROUP BY New_details.name
ORDER BY avg_quantity ASC;
 