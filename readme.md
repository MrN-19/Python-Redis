# Python Redis Databse Simulation

## Introdcution

This Project Designed by Python to Simulate Redis Database Function

## Description

This Project Runs On Network , We Wanted Simulate this Project to Redis Database Completly , becouse of This We use 
Of Socket Concept to Run This Project On Network and Accessed On 6379 Port

## What Is Redis ?

Redis Is a No Sql Database that Uses Of System Memory to Store Data for Limited Time , Becouse of This Concept , Its Very Fast
Data in This Database Stored In (Key,Value) format 

## How To Use Of This Project ?

1. in the first Step you Should Clone this Project from [This Url](https://github.com/MrN-19/Python-Redis.git)
2. this Project Doesnt Need any external library or packages
3. after you cloned the project , you will see two python file in the root of project

4. ### redis_server.py :
    this file is server side of project, for running this you should just run like a simple python file based on your machine
    this file uses of socket module to run on the network that accessed on `127.0.0.1:6379` or localhost

    when you runned this file , you should do anything , this file will handle everything

5. ## redis_client.py :

    this file is client side of project , running this file is like running `redis_server.py` file , 
    actually this file after running , will connect to `127.0.0.1:6379` and recives redis commands 
    and send them to server side of project to run commands


## What This Project Do ?

This Project Simulates Redis Database Commands , Something Like `Build Your Own Redis With C\C++` Book , but we Simulate it by Python

We have Some Basic Commands for `String` datatype in redis `get` and `set` commands are commands to set a new variable to databse with specific key and value

### Example : 

`set name mohammadreza` This command set new string variable with `name` key and `mohammadreza` value <br>
Now We can get `mohammadreza` value with `get name` command , definitly you know that no key shouldnt be repeated more than once
# Hope to Enjoy !

this project can be good practice for python developers who has already started to learn python programming language

I Hope to Enjoy this Project and Rate it !

