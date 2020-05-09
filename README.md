# Orinoco Database Assessment

## Introduction

Within this assessment we were given the task of creating, extending and manipulating data within a relational database to further develop an understanding of SQL and its application to real world scenarios.

Within this report I will be discussing the theory and importance of relational databases in todays modern world, as well as assessing and evaluating my own queries that I have written.

---

## Theory

### Key issues in the development of relational databases

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

### The use of SQL functionality to create information from data

ADD THIS SHIT HERE

---

## Practical

### 1. Retrieving Data using SQL

#### Query 01

A marketing campaign query to find new shoppers and those who are aged under 30. This query is responsible for retrieve the shoppers:

- First Name
- Surname
- Email Address
- Date Joined (formatted into DD-MM-YY)
- Age in years (converted from birth date into an int)

Of all shoppers who joined on or after 01-01-2020 OR those aged 29 or less on 01-01-2020. Ordered by by age (highest first) and then surname (A-Z).

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

#### Query 02

A customer account history page query which will accept the shopper id as a parameter to display corresponding information. Used to retrieve the:

- First Name
- Surname of specified shopper
- Order no
- Ordered product status
- Order Date (Formatted dd-mm-yy)
- Product Description
- Seller name
- Quantity ordered
- Price (two decimal places with a £ sign)
- Ordered product status

To get all of the data stated above I needed to Inner Join the initial shoppers table with 4 others, including:

- shopper_orders Table
- ordered_products Table
- products Table
- sellers Table

Finally ordering the data by date, showing the most recent order first. And tested through using shopper ids 10000 and 10019.

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

#### Query 03

A query written to produce a summary report on the sellers and products that they have had sold since 01-06-2019. Displaying and retriving the:

- Seller account ref
- Seller Name
- Product Code
- Product Description
- Number of Orders
- Total quantity sold
- Total value of all sales (two decimal places with a £)

Including products that a seller sells but has had no orders for AND showing any NULL values as 0. Achieved by left Outer Joining the folling tables to my initial sellers table:

- products
- ordered_products
- shopper_orders

Grouping the results by seller name and then product description.

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

---

### 2. Database Design, Implementation and Integrity

#### Table Design 01

This table takes the main elements of what would be required for any review and documents every required field into its own column of data. With the addition of the seller_id to associate every review with the corresponding seller, as well as the shopper_id to identify which user has left the review, allowing for possible follow up or personalised responses based on their review.

| Seller Review Table     | Type          | KEY | Description                                                |
| ----------------------- |:-------------:|:---:| ---------------------------------------------------------- |
| seller_review_id        | INTEGER       | PK  | Unique Primary key to identify seller reviews              |
| seller_id               | INTEGER       | FK  | Foreign Key To Identify the seller review is written about |
| shopper_id              | INTEGER       | FK  | Foreign Key To Identify the shopper who wrote review       |
| seller_review_desc      | TEXT          |     | The textual description of the seller review               |
| seller_review_rating    | TEXT          |     | The rating given to seller strictly ranging from *-*****   |
| seller_review_date_time | DATE          |     | The Date and time the review was made                      |

#### Table Design 02

This table also takes the main elements of what would be required for any review and documents every required field into its own column of data. With the addition of the product_id to associate every review with the corresponding product, as well as the shopper_id to identify which user has left the review, allowing for possible follow up or personalised responses based on their review.

| Product Review Table     | Type          | KEY | Description                                                 |
| ------------------------ |:-------------:|:---:| ----------------------------------------------------------- |
| product_review_id        | INTEGER       | PK  | Unique Primary key to identify product reviews              |
| product_id               | INTEGER       | FK  | Foreign Key To Identify the product review is written about |
| Shopper_id               | INTEGER       | FK  | Foreign Key To Identify the shopper who wrote review        |
| product_review_desc      | TEXT          |     | The textual description of the product review               |
| product_review_rating    | TEXT          |     | The rating given to seller strictly ranging from *-*****    |
| product_review_date_time | DATE          |     | The Date and time the review was made                       |

#### Table Design 03

The questions table would extend off of the pre existing  products table and be connected to it through the product_id foreign key as to uniquely link all questions to their products. Questions would consist only of descriptions and the date they were posted. They should all be uniquely identified ny their question ID as well. There is no shopper_id since questions are able to be asked annonomously as stated in our brief.

| Questions          | Type    | KEY | Description                                                   |
| ------------------ |:-------:|:---:| ------------------------------------------------------------- |
| question_id        | INTEGER | PK  | Unique Primary key to identify product Questions              |
| product_id         | INTEGER | FK  | Foreign Key To Identify the product question is written about |
| question_desc      | TEXT    |     | The textual description of the product question               |
| question_date_time | DATE    |     | The Date and time the question was asked                      |

#### Table Design 04

The answer will all be uniquely identified by the answer_id and associated to the question through the question_id foreign key. To ensure that the answers can be traced back to the shopper or seller who left the reponse, I added both the seller_id and the shopper_id as foreign keys. The question itself will again only exist of a descriptive text and date it will be posted.

| Answers         | Type    | KEY | Description                                           |
| --------------- |:-------:|:---:| ----------------------------------------------------- |
| answer_id       | INTEGER | PK  | Unique Primary key to identify product Answers        |
| question_id     | INTEGER | FK  | Foreign Key To Identify the corresponding question    |
| shopper_id      | INTEGER | FK  | Foreign Key To Identify the shopper who wrote Answers |
| seller_id       | INTEGER | FK  | Foreign Key To Identify the seller who wrote review   |
| answer_text     | TEXT    |     | The textual description of the question answer        |
| submission_date | DATE    |     | The Date and time the answer was posted               |

---

#### Electronic Relationship Diagram

This modified ERD displays how the new tables would be connected and extend the current architecture, allowing for a simplified and expandable view that could immediately be implimented if needed. There are a total of 4 new tables added to the existing design and justification for each can be found abovve

![ERD](https://i.imgur.com/nVw9f6y.png)

---

#### SQL Table Create Queries

In this section I am demonstrating how I created my additional tables through create queries,afterwards insert dummy data rows into the newly creates tables to facilitate testing and prove that your integrity constraints work correctly through the testing process.

##### Seller Review Table

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

##### Product Review Table

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

##### Questions Table

``` SQL
CREATE TABLE questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id  INTEGER REFERENCES products(products_id),
    question_desc TEXT NOT NULL,
    question_date_time DATE NOT NULL,
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

##### Answers Table

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
