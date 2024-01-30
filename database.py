import mysql.connector as conn
from tool_ import loadConfig

def create_db(database="test"):
    con=conn.connect(
        host=loadConfig()['host'],
        user=loadConfig()['user'],
        password=loadConfig()['pass'],
    )
    cur= con.cursor()
    sql="CREATE DATABASE IF NOT EXISTS "+database
    cur.execute(sql)
    # create_table(database="tetludb")

def connect_db(database="santhitdb"):
    create_db(database)
    con=conn.connect(
        host=loadConfig()['host'],
        user=loadConfig()['user'],
        password=loadConfig()['pass'],
        database=database
    )
    return con
def create_tables():
    con=connect_db()
    cur=con.cursor()

    ########### employee ###########
    sql="""
CREATE TABLE IF NOT EXISTS `employee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empid` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `dob` varchar(45) DEFAULT '**data required**',
  `nrc` varchar(30) DEFAULT '**data required**',
  `gender` varchar(15) NOT NULL,
  `contact` varchar(50) NOT NULL,
  `salary` varchar(10) NOT NULL,
  `usertype` varchar(45) NOT NULL,
  `address` varchar(500) DEFAULT '**data required**',
  PRIMARY KEY (`id`)
)

"""
    cur.execute(sql)
    con.commit()
    #print("employee table created")

    ########### supplier ###########
    sql="""
CREATE TABLE IF NOT EXISTS `supplier` (
  `id` int NOT NULL AUTO_INCREMENT,
  `supid` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `contact` varchar(50) NOT NULL,
  `companyName` varchar(500) NOT NULL,
  `companyPhone` varchar(50) NOT NULL,
  `address` varchar(500) DEFAULT '**data required**',
  `remark` varchar(100) NOT NULL,
   PRIMARY KEY (`id`)
)

"""

    cur.execute(sql)
    con.commit()
    #print("supplier table created")
########### customer ###########
    sql="""
CREATE TABLE IF NOT EXISTS `customer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cusid` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `contact` varchar(50) NOT NULL,
  `custype` varchar(50) NOT NULL,
  `address` varchar(500) DEFAULT '**data required**',
  `remark` varchar(100) NOT NULL,
   PRIMARY KEY (`id`)
)

"""

    cur.execute(sql)
    con.commit()
    #print("customer table created")
########### category ###########
    sql="""
CREATE TABLE IF NOT EXISTS `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `catid` varchar(30) NOT NULL,
  `name` varchar(50) NOT NULL,
   PRIMARY KEY (`id`)
)

"""

    cur.execute(sql)
    con.commit()
    #print("category table created")
    
########### product ###########
    sql="""
CREATE TABLE IF NOT EXISTS `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pid` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `description` varchar(500) NOT NULL,
  `qty` varchar(100) DEFAULT 'n/a',
  `price` varchar(100) DEFAULT 'n/a',
  `status` varchar(100) DEFAULT 'active',

  `category` varchar(100) NOT NULL,
  `supplier` varchar(100) DEFAULT '**data required**',
  `created_time` varchar(30) DEFAULT '**data required**',
  `remark` varchar(100) NOT NULL,
   PRIMARY KEY (`id`)
)

"""
    cur.execute(sql)
    con.commit()
    #print("product table created")

    sql="""
CREATE TABLE IF NOT EXISTS `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `userid` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT '**data required**',
  `status` varchar(50) NOT NULL,
  `created_time` varchar(30) DEFAULT '**data required**',
  `usertype` varchar(50) NOT NULL,

   PRIMARY KEY (`id`)
)

"""
    cur.execute(sql)
    con.commit()


    sql="""
CREATE TABLE IF NOT EXISTS buy (
  id int NOT NULL AUTO_INCREMENT,
  pid varchar(45) NOT NULL,
  buyid varchar(45) NOT NULL,
  name varchar(100) NOT NULL,
  description varchar(300) NOT NULL,
  category varchar(50) NOT NULL,
  cost varchar(50) NOT NULL,
  quantity varchar(45) NOT NULL,
  supplier varchar(100) NOT NULL,
  date varchar(50) NOT NULL,
  expdate varchar(50) NOT NULL,
   PRIMARY KEY (id)
)

"""
    cur.execute(sql)
    con.commit()    


    sql="""    
CREATE TABLE IF NOT EXISTS saleorder (
  sr int NOT NULL AUTO_INCREMENT,
  voucherid VARCHAR(45) NOT NULL,
  cid VARCHAR(45) NOT NULL,
  cname VARCHAR(100) NOT NULL,
  pid VARCHAR(45) NOT NULL,
  qty VARCHAR(45) NOT NULL,
  date VARCHAR(45) NOT NULL,
  total VARCHAR(45) NOT NULL,
  PRIMARY KEY (`sr`))
"""
    cur.execute(sql)
    con.commit()

    sql="""
CREATE TABLE IF NOT EXISTS wallet(
id int NOT NULL AUTO_INCREMENT,
walid varchar(45) NOT NULL,
description varchar(200) NOT NULL,
deposit varchar(50) NOT NULL,
withdraw varchar(50) NOT NULL,
balance varchar(50) NOT NULL,
date varchar(50) NOT NULL,
PRIMARY KEY(id)
)
"""
    cur.execute(sql)
    con.commit()