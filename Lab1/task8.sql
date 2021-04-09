-- Создать запрос для модификации всех значений столбца с суммарной величиной платы,
-- чтобы он содержал истинную сумму, которую заплатил потребитель ( с учетом скидки).
-- Вывести новые значения.
UPDATE "Order" SET amount = amount*(1 - discount / 100) FROM Customer WHERE customer = Customer.ID;
SELECT amount FROM "Order"