# Orinoco Database Assessment

## Introduction

Within this assessment we were given the task of creating, extending and manipulating data within a relational database to further develop an understanding of SQL and its application to real world scenarios.

Within this report I will be discussing the theory and importance of relational databases in todays modern world, as well as assessing and evaluating my own queries that I have written.

## Theory

---

### 1. Key issues in the development of relational databases.

Transaction Reliability	
Guarantees very high transaction reliability as they fully support ACID properties
Do not guarantee very high reliability as they range from BASE to ACID properties

Performance
Caching has to be done with special infrastructure support
Performance is enhanced by caching data into system memory

Indexing
Index available on multiple column
Single index, key-value store

Data Model
Data model is very specific and well organized. Columns and rows are described by well-defined schema
Data model does not use the table as storage structure and is schema less. Data model is very efficient in handling unstructured data as well

Scalability
Scalability is greatest challenge in relational databases due to the dependency on vertical scalability
NoSQL databases depend on horizontal scalability

Cloud
Not suitable for cloud environment as these databases do not support data search on full content. Relational databases are also very hard to extend beyond a limit
Well suited for cloud databases. All characteristics of NoSQL databases [10] are highly desirable for cloud databases

Handling Big Data
Big Data handling is a challenging issue for relational databases
NoSQL databases are designed to handle Big Data

Data Warehouse
When the size of stored data increases, problems related to performance degradation raises
NoSQL databases are not designed to serve data warehouse. NoSQL databases are faster than data warehouse

Complexity
Complexity arises due to nonfixture of data into tables
NoSQL databases have the capabilities to store unstructured data
Crash Recovery
They guarantee crash recovery through recovery manager
NoSQL databases use replication method as backup to recuperate from crash
Authentication
Relational databases come with authentication mechanism
NoSQL database does not have strong authentication mechanism and are dependent on external method for this

Data Integrity
Relational databases ensure data integrity
A NoSQL database does not support data integrity at every occasion
Confidentiality
Data confidentiality is a well-known feature of relational database
Generally data confidentiality is not achieved in NoSQL databases
Auditing
Relational databases provide mechanisms to audit database
Most of the NoSQL databases do not provide mechanism for auditing the database

### 2. The use of SQL functionality to create information from data

## Practical Development Work

The practical development work is based on an online electronics shopping company where you work as a Database Analyst/Developer. The entity-relationship diagram and SQL script for creating and populating the database are provided on SOL. 

### 1. Retrieving Data using SQL

#### Query 01

company want to do a marketing campaign to new shoppers and those aged under 30. Retrieve the first name, surname, email address, date joined, and the age in years of all shoppers who joined on or after 1st Jan 2020 or those aged 29 or less on the 1st Jan 2020. Print date columns in the format DD-MM-YYYY. Order results by age (highest first) and then surname (A-Z).

``` SQL
SELECT  shopper_first_name as Name,
        shopper_surname as Surname,
        shopper_email_address as Email,
        strftime('%d/%m/%Y',date_joined) as JoinDate,
        cast(strftime('%Y.%m%d', '2020-01-01') - strftime('%Y.%m%d', date_of_birth) as int) as Age
FROM shoppers
WHERE date_of_birth > '1990-01-01'  OR date_joined > '2020-01-01'
ORDER BY Age DESC, shopper_surname ASC
```

---

#### Query 02

website requires a customer account history page which will accept the shopper id as a parameter. Write a query to retrieve the first name and surname for a specific shopper along with details of all the orders they’ve placed, displaying the order no, order date, product description, seller name, quantity ordered, price (right-justified with two decimal places and prefixed by a £ sign) and ordered product status. Print date columns in the format DD-MM-YYYY. Sort the results by order date showing the most recent order first. Test your query by prompting for the user to input a shopper account ref and produce results for shopper ids 10000 and 10019.

``` SQL
SELECT  shoppers.shopper_first_name as Name,
        shoppers.shopper_surname as Surname,
        shopper_orders.order_id as OrderNum,
        strftime('%d/%m/%Y',shopper_orders.order_date) as Date,
        ordered_products.quantity as Amount,
        PRINTF("£%7.2f", ordered_products.price) AS 'Price',
        ordered_products.ordered_product_status as Status,
        products. product_description as Description,
        sellers.seller_name as Seller

FROM shoppers
    INNER JOIN shopper_orders ON shoppers.shopper_id = shopper_orders.shopper_id
    INNER JOIN ordered_products ON shopper_orders.order_id = ordered_products.order_id
    INNER JOIN products ON ordered_products.product_id = products.product_id
    INNER JOIN sellers ON ordered_products.seller_id = sellers.seller_id

WHERE shoppers.shopper_id = 10000 OR shoppers.shopper_id = 10019

ORDER BY Name, shopper_orders.order_date DESC
```

---

#### Query 03

business relationship manager has asked you to write a summary report on the sellers and products that they have had sold since 1st June 2019. Display the seller account ref, seller name, product code, product description, number of orders, total quantity sold and total value of all sales (right-justified with two decimal places and prefixed by a £ sign) for each product they sell. You should also include products that a seller sells but has had no orders for and show any NULL values as 0. Sort results by seller name and then product description.

``` SQL
SELECT  sellers.seller_account_ref AS ACCOUNT,
        sellers.seller_name AS SellerName, 
        products.product_id AS ProductID, 
        products.product_description AS Desc,
        IFNULL(ordered_products.quantity, '0') AS Amount,
        PRINTF("£%7.2f",SUM(ordered_products.price*ordered_products.quantity)) AS TotalValue,
        IFNULL(COUNT(ordered_products.order_id), '0') AS AmountSold

FROM sellers
    INNER JOIN product_sellers ON sellers.seller_id = product_sellers.seller_id
    LEFT OUTER JOIN products ON product_sellers.product_id = products.product_id
    LEFT OUTER JOIN ordered_products ON product_sellers.product_id = ordered_products.product_id
    LEFT OUTER JOIN shopper_orders ON ordered_products.order_id = shopper_orders.order_id

WHERE shopper_orders.order_date >= '2019-06-01' OR shopper_orders.order_date IS NULL

GROUP BY sellers.seller_name, products.product_description
```

### 2. Database Design, Implementation and Integrity

Produce a table design to support this additional functionality explaining the process you used to arrive at your design, how you ensured the database integrity would be maintained and any design assumptions that you have made. Your design should consist of at least two new tables and you must link to at least one of the existing tables.

| Seller Review Table     | Type          | KEY   | Description                                                |
| ----------------------- |:-------------:|:-----:| ---------------------------------------------------------- |
| seller_review_id        | INTEGER       | PK    | Unique Primary key to identify seller reviews              |
| seller_id               | INTEGER       | FK    | Foreign Key To Identify the seller review is written about |
| shopper_id              | INTEGER       | FK    | Foreign Key To Identify the shopper who wrote review       |
| seller_review_desc      | TEXT          |       | The textual description of the seller review               |
| seller_review_rating    | TEXT          |       | The rating given to seller strictly ranging from *-*****   |
| seller_review_date_time | DATE          |       | The Date and time the review was made                      |

| Product Review Table     | Type          | KEY   | Description                                                 |
| ------------------------ |:-------------:|:-----:| ----------------------------------------------------------- |
| product_review_id        | INTEGER       | PK    | Unique Primary key to identify product reviews              |
| product_id               | INTEGER       | FK    | Foreign Key To Identify the product review is written about |
| Shopper_id               | INTEGER       | FK    | Foreign Key To Identify the shopper who wrote review        |
| product_review_desc      | TEXT          |       | The textual description of the product review               |
| product_review_rating    | TEXT          |       | The rating given to seller strictly ranging from *-*****    |
| product_review_date_time | DATE          |       | The Date and time the review was made                       |

Modify the provided Entity Relationship diagram to show your new tables, their primary and foreign keys and how they relate to each other and to the existing tables.

IMAGE HERE

Implement your design by creating the new tables, insert enough rows into your new tables to facilitate testing and prove that your integrity constraints work correctly through testing. Include the SQL that you used to create, populate and test the new tables in your submission

#### Seller Review Table

``` SQL
CREATE TABLE seller_review
(
     seller_review_id INTEGER PRIMARY KEY AUTOINCREMENT,
     seller_id  INTEGER REFERENCES sellers(seller_id),
     shopper_id  INTEGER REFERENCES shoppers(shopper_id),
     seller_review_desc TEXT NOT NULL,
     seller_review_rating TEXT NOT NULL,
     seller_review_date_time DATE NOT NULL
     CONSTRAINT seller_review_rating CHECK (seller_review_rating IN ('*','**','***','****','*****')),
     CONSTRAINT seller_review_seller_fk FOREIGN KEY (seller_id)
                             REFERENCES sellers (seller_id),
     CONSTRAINT seller_review_shopper_fk FOREIGN KEY (shopper_id)
                             REFERENCES shoppers (shopper_id)
);

INSERT INTO seller_review (
                              seller_review_id,
                              seller_id,
                              shopper_id,
                              seller_review_desc,
                              seller_review_rating,
                              seller_review_date_time
                          )
                          VALUES (
                              '1',
                              '200000',
                              '10000',
                              'Review 01',
                              '***',
                              '20200101 10:10:10 AM'
                          );
INSERT INTO seller_review (
                              seller_review_id,
                              seller_id,
                              shopper_id,
                              seller_review_desc,
                              seller_review_rating,
                              seller_review_date_time
                          )
                          VALUES (
                              '2',
                              '200000',
                              '10001',
                              'Review 02',
                              '*****',
                              '20200101 10:10:10 AM'
                          );
```

#### Product Review Table

``` SQL
CREATE TABLE product_review
(
     product_review_id INTEGER PRIMARY KEY AUTOINCREMENT,
     product_id  INTEGER REFERENCES products(seller_id),
     shopper_id  INTEGER REFERENCES shoppers(shopper_id),
     product_review_desc TEXT NOT NULL,
     product_review_rating TEXT NOT NULL,
     product_review_date_time DATE NOT NULL
     CONSTRAINT product_review_rating CHECK (product_review_rating IN ('*','**','***','****','*****')),
     CONSTRAINT product_review_product_fk FOREIGN KEY (product_id)
                             REFERENCES products (product_id),
     CONSTRAINT product_review_shopper_fk FOREIGN KEY (shopper_id)
                             REFERENCES shoppers (shopper_id)
);

INSERT INTO product_review (
                               product_review_id,
                               product_id,
                               shopper_id,
                               product_review_desc,
                               product_review_rating,
                               product_review_date_time
                           )
                           VALUES (
                               '1',
                               '300000',
                               '10000',
                               'Review 01',
                               '*',
                               '20200101 10:10:10 AM'
                           );
INSERT INTO product_review (
                               product_review_id,
                               product_id,
                               shopper_id,
                               product_review_desc,
                               product_review_rating,
                               product_review_date_time
                           )
                           VALUES (
                               '2',
                               '300001',
                               '10000',
                               'Review 02',
                               '*****',
                               '20200101 10:10:10 AM'
                           );
```

#### Questions Tablle

``` SQL
CREATE TABLE questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id  INTEGER REFERENCES products(products_id),
    question_desc TEXT NOT NULL,
    question_date_time TEXT NOT NULL,
    CONSTRAINT questions_fk FOREIGN KEY (product_id)
                             REFERENCES products (product_id)
);

INSERT INTO questions (
                          question_id,
                          product_id,
                          question_desc,
                          question_date_time
                      )
                      VALUES (
                          '1',
                          '3000000',
                          'Question 01',
                          '20200101 10:10:10 AM'
                      );
INSERT INTO questions (
                          question_id,
                          product_id,
                          question_desc,
                          question_date_time
                      )
                      VALUES (
                          '2',
                          '3000001',
                          'Question 02',
                          '20200101 10:10:10 AM'
                      );
```

#### Answers Table

``` SQL
CREATE TABLE answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER REFERENCES questions(question_id ),
    shopper_id  INTEGER REFERENCES shoppers(shopper_id),
    seller_id  INTEGER REFERENCES sellers(seller_id),
    answer_text TEXT NOT NULL,
    submission_date DATE NOT NULL,
    CONSTRAINT answers_questions_fk FOREIGN KEY (question_id)
                             REFERENCES questions (question_id),
    CONSTRAINT answers_seller_fk FOREIGN KEY (seller_id)
                             REFERENCES sellers (seller_id),
    CONSTRAINT seller_review_fk FOREIGN KEY (shopper_id)
                             REFERENCES shoppers (shopper_id)                       
);

INSERT INTO answers (
                        answer_id,
                        question_id,
                        shopper_id,
                        seller_id,
                        answer_text,
                        submission_date
                    )
                    VALUES (
                        '1'
                        '1',
                        '100000',
                        '200000',
                        'Answer 01 Q1',
                        '20200101 10:10:10 AM'
                    );
INSERT INTO answers (
                        answer_id,
                        question_id,
                        shopper_id,
                        seller_id,
                        answer_text,
                        submission_date
                    )
                    VALUES (
                        '2'
                        '1',
                        '100000',
                        '200000',
                        'Answer 02 Q1',
                        '20200101 10:10:10 AM'
                    );


INSERT INTO answers (
                        answer_id,
                        question_id,
                        shopper_id,
                        seller_id,
                        answer_text,
                        submission_date
                    )
                    VALUES (
                        '3'
                        '2',
                        '100001',
                        '200001',
                        'Answer 01 Q2',
                        '20200101 10:10:10 AM'
                    );
INSERT INTO answers (
                        answer_id,
                        question_id,
                        shopper_id,
                        seller_id,
                        answer_text,
                        submission_date
                    )
                    VALUES (
                        '4'
                        '2',
                        '100001',
                        '200001',
                        'Answer 02 Q2',
                        '20200101 10:10:10 AM'
                    );
```

### 3. Programming for Databases
