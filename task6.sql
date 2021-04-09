-- На основании данных о заказах вывести все данные в таком формате:
-- a) номер, дата фамилия поставщика, сумма заказа. Отсортировать по фамилиям и сумме заказа;
SELECT number, date, surname, amount FROM "Order", Supplier WHERE supplier = Supplier.ID
ORDER BY surname, amount ASC;


-- b) название детали, количество, дата.
SELECT name, Detail.quantity, date FROM "Order", Detail WHERE detail = Detail.ID;