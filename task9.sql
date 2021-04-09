-- Расширить таблицу с данными о заказах столбцом, содержащим величину комиссионных поставщика.
-- Создать запрос для ввода конкретных значений во все строки таблицы.
ALTER TABLE "Order" ADD COLUMN "commission amount" NUMERIC(18, 2) DEFAULT 0;
UPDATE "Order" SET "commission amount" = amount*(commission / 100)
FROM Supplier WHERE supplier = Supplier.ID;
SELECT * FROM "Order";