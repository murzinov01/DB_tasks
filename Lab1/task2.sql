-- Ввести в ранее созданные таблицы конкретные данные (см. прил. 1).
-- Использовать скрипт-файл из операторов INSERT или вспомогательную утилиту .
INSERT INTO Customer (ID, name, address, discount) VALUES (001, 'АО ВАРЯ', 'Сормовский', 10);
INSERT INTO Customer (ID, name, address,discount) VALUES (002, 'ГАЗ', 'Автозаводский', 7);
INSERT INTO Customer (ID, name, address,discount) VALUES (003, 'МП ВЕРА', 'Канавинский', 5);
INSERT INTO Customer (ID, name, address,discount) VALUES (004, 'МП', 'Канавинский', 4);
INSERT INTO Customer (ID, name, address,discount) VALUES (005, 'АО СТАЛЬ', 'Советский', 0);
-- 001	АО ВАРЯ	Сормовский	10
-- 002	ГАЗ	Автозаводский	7
-- 003	МП ВЕРА	Канавинский	5
-- 004	МП	Канавинский	3
-- 005	АО СТАЛЬ	Советский	0


INSERT INTO Supplier (ID, surname, address, commission) VALUES (001, 'Артюхина', 'Сормовский', 4);
INSERT INTO Supplier (ID, surname, address, commission) VALUES (002, 'Щепин', 'Приокский', 4);
INSERT INTO Supplier (ID, surname, address, commission) VALUES (003, 'Власов', 'Канавинский', 5);
INSERT INTO Supplier (ID, surname, address, commission) VALUES (004, 'Кузнецова', 'Советский', 5);
INSERT INTO Supplier (ID, surname, address, commission) VALUES (005, 'Цепилева', 'Нижегородский', 3);
INSERT INTO Supplier (ID, surname, address, commission) VALUES (006, 'Корнилов', 'Нижегородский', 6);
-- 001	Артюхина	Сормовский	4
-- 002	Щепин	Приокский	4
-- 003	Власов	Канавинский	5
-- 004	Кузнецова	Советский	5
-- 005	Цепилева	Нижегородский	3
-- 006	Корнилов	Нижегородский	6


INSERT INTO Detail (ID, name, storage, quantity, price) VALUES (001, 'Втулка', 'Сормовский', 20000, 5000);
INSERT INTO Detail (ID, name, storage, quantity, price) VALUES (002, 'Болт', 'Сормовский', 40000, 1000);
INSERT INTO Detail (ID, name, storage, quantity, price) VALUES (003, 'Ключ гаечный', 'Канавинский', 5000, 3000);
INSERT INTO Detail (ID, name, storage, quantity, price) VALUES (004, 'Шпилька', 'Автозаводский', 10000, 900);
INSERT INTO Detail (ID, name, storage, quantity, price) VALUES (005, 'Винт', 'Сормовский', 50000, 1500);
INSERT INTO Detail (ID, name, storage, quantity, price) VALUES (006, 'Молоток', 'Канавинский', 1200, 2000);
INSERT INTO Detail (ID, name, storage, quantity, price) VALUES (007, 'Шуруп', 'Сормовский', 30000, 1200);
-- 001	Втулка	Сормовский	20000	5000
-- 002	Болт	Сормовский	40000	1000
-- 003	Ключ гаечный	Канавинский	5000	3000
-- 004	Шпилька	Автозаводский	10000	900
-- 005	Винт	Сормовский	50000	1500
-- 006	Молоток	Канавинский	1200	2000
-- 007	Шуруп	Сормовский	30000	1200


INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00001, 'Январь',  005, 004, 003, 7, 21000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00002, 'Февраль', 003,	003, 003, 2, 6000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00003, 'Февраль', 004,	005, 004, 200, 180000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00004, 'Март',    005, 004, 002, 50, 50000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00005, 'Апрель',  001, 006, 007, 110, 132000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00006, 'Апрель',  004, 004, 001, 150, 750000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00007, 'Май',     002,	004, 006, 20, 40000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00008, 'Июнь',    001, 003, 007, 2000,	2400000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00009, 'Июнь',    002, 005, 007, 10000, 12000000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00010, 'Июнь',    003, 006, 001, 5, 25000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00011, 'Июнь',    004, 003, 003, 1, 3000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00012, 'Июнь',    004, 004, 001, 10, 50000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00013, 'Июль',    001, 006, 006, 3, 6000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00014, 'Июль',    002, 001, 002, 1000,	1000000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00015, 'Июль',    002, 002, 001, 100, 5000000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00016, 'Июль',    005, 001, 005, 100, 15000);
INSERT INTO "Order" (number, date, customer, supplier, detail, quantity, amount) VALUES (00017, 'Август',  001, 004, 007, 12000, 24400000);
-- 00001	Январь	005	004	003	7	21000
-- 00002	Февраль	003	003	003	2	6000
-- 00003	Февраль	004	005	004	200	180000
-- 00004	Март	005	004	002	50	50000
-- 00005	Апрель	001	006	007	110	132000
-- 00006	Апрель	004	004	001	150	750000
-- 00007	Май	002	004	006	20	40000
-- 00008	Июнь	001	003	007	2000	2400000
-- 00009	Июнь	002	005	007	10000	12000000
-- 00010	Июнь	003	006	001	5	25000
-- 00011	Июнь	004	003	003	1	3000
-- 00012	Июнь	004	004	001	10	50000
-- 00013	Июль	001	006	006	3	6000
-- 00014	Июль	002	001	002	1000	1000000
-- 00015	Июль	002	002	001	100	5000000
-- 00016	Июль	005	001	005	100	15000
-- 00017	Август	001	004	007	12000	24400000