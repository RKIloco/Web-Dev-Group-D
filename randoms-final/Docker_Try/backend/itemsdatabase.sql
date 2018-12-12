Create Database itemsdatabase;
use itemsdatabase ;

CREATE TABLE  Item (
    item_id Int Not NULL PRIMARY KEY AUTO_INCREMENT ,
    name VARCHAR(80) unique NOT NULL,
    price Int NOT NULL,
    seller_name VARCHAR(80) NOT NULL,
    link varchar(1000)
);


CREATE TABLE History (
    history_id Int Not NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(80) unique NOT NULL,
    price Int NOT NULL,
    buyer_name VARCHAR(80) NOT NULL,
    seller_name VARCHAR(80) NOT NULL,
    link varchar(1000)
);


CREATE TABLE Account (
    account_id Int Not NULL PRIMARY KEY AUTO_INCREMENT ,
    username VARCHAR(80) unique NOT NULL,
    password varchar(150) unique not null
);


CREATE TABLE loggedin (
    account_id Int Not NULL PRIMARY KEY AUTO_INCREMENT ,
     username VARCHAR(80) unique NOT NULL
);

