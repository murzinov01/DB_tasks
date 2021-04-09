-- Используя операцию UNION получить места складирования деталей и места расположения поставщиков.
SELECT storage
FROM Detail
UNION
SELECT address
FROM Supplier