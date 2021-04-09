-- Создав запрос получить следующую информацию:
-- a) фамилии и адреса поставщиков, имеющих размер комиссионных менее 5%;
SELECT surname, address FROM Supplier WHERE commission < 5;


-- b) название и адрес склада для деталей, находящихся в количесиве менее 1500 шт.;
SELECT name, storage FROM Detail WHERE quantity < 1500;


-- c) название, адрес и размер скидки для предприятий, имеющих в названии слово “МП”.
-- Отсортировать по адресу и размеру скидки.
SELECT name, address, discount FROM Customer WHERE name LIKE '%МП%'
ORDER BY address, discount;