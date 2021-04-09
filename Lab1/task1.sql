-- Дана схема базы данных в виде следующих отношений.
-- С помощью операторов SQL создать логическую структуру соответствующих таблиц для хранения в СУБД,
-- используя известные средства поддержания целостности (NOT NULL, UNIQUE, и т.д.).
-- Обосновать выбор типов данных и используемые средства поддержания целостности. 
-- При выборе подходящих типов данных использовать информацию о конкретных значениях полей БД (см. прил.1)
CREATE TABLE Customer
(ID   INT  PRIMARY KEY,
 name VARCHAR(255) NOT NULL,
 address TEXT NOT NULL,
 discount FLOAT NOT NULL CHECK (discount>=0 AND discount<=100)
);

CREATE TABLE Supplier
(ID   INT  PRIMARY KEY,
 surname VARCHAR(255) NOT NULL,
 address TEXT NOT NULL,
 commission FLOAT NOT NULL CHECK (commission>=0 AND commission<=100)
);

CREATE TABLE Detail
(ID   INT  PRIMARY KEY,
 name VARCHAR(255) NOT NULL,
 storage TEXT NOT NULL,
 quantity INT NOT NULL CHECK (quantity>=0),
 price NUMERIC(18, 2) NOT NULL CHECK (price>=0)
);

CREATE TABLE "Order"
(number   INT  PRIMARY KEY,
 date CHAR(20) NOT NULL,
 customer INT NOT NULL,
 supplier INT NOT NULL,
 detail INT NOT NULL,
 quantity INT NOT NULL CHECK (quantity>=0),
 amount NUMERIC(18, 2) NOT NULL CHECK (amount>=0),
 FOREIGN KEY (customer)  REFERENCES Customer (ID),
 FOREIGN KEY (supplier)  REFERENCES Supplier (ID),
 FOREIGN KEY (detail)  REFERENCES Detail (ID)
);