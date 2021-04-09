-- Создать запросы для вывода:
-- a) всех различных размеров комиссионных;
SELECT DISTINCT commission FROM Supplier
ORDER BY commission ASC;


-- b) всех различных фамилий поставщиков;
SELECT DISTINCT surname FROM Supplier
ORDER BY surname ASC;


-- c) всех различных наименований деталей.
SELECT DISTINCT name FROM Detail
ORDER BY name ASC;