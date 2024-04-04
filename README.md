# VALENTIN’S COMMENTS SYSTEM
## Video Demo: https://youtu.be/qQpSwAHKnR8
## Description:

For my project, I created a program that allows the user to create an account and login into the system, create topics where others can express their opinions and ideas, and explore other topics.
Basically, when the user has an account and it’s logged in the system, he will be able to create topics for him and others to discuss, explore other topics and the comments made by different users, and comment every time he wants to.

The file called **“project.py”** stores all the code and functions needed for the program to run correctly (functions, classes and imported libraries).
Additionally, there is a file called **“test_project.py”**, which contains test functions to verify the functionality and reliability of key components.
I chose the different validation functions (username, password, topic name and comment validation) because they are the ones that actually return a value depending on the situation.

## Introduction to the program

Firstly, the program tries to automatically **login with the last account used**, but if there isn’t any, a menu will be displayed where the user can **login**, **register** or **exit the system** (the exit option ends the execution of the program).

### Registering an account and logging into the system

The user can’t login if there is not an account saved in the system ("users.csv") and **cannot register with a username that is already registered**. If it’s the first time registering an account, a file called **“users.csv”** that saves usernames and passwords will be created.
Also, when a user logins, it will create a file called **“last_user.csv”** where the last used account will be saved (to automatically login when the program is started again).

### Username and password validation

The username must be **between 4 and 15 characters** (which can only be letters, numbers and underscores), while the password must contain **at least 6 characters** (which cannot include quotation marks nor spaces).

## Once logged in

When the user is logged in the system, another menu will be displayed, where he can **explore the different topics** (stored in "topics.csv") and **comments** (saved in "comments.csv") **and even comment**, **create a topic of his interest**, **log out**, and **exit the system** (closing the program). If the user logs out, **“last_user.csv”** will be deleted to prevent automatic login upon restarting the program.

### Creating topics

The user cannot explore the topics if there aren’t any.
**If he wants to create a topic, its name must be between 10 and 50 characters**. One important thing is that **a user can’t have more than one topic with the same name**.
The first time a topic is made in the system, a file called **“topics.csv”** that stores each topic’s name, its creator username and the creation date, is created to save it and the rest of the topics.

### Exploring the system and making comments

If there are topics saved, the user can explore them, see the different comments made in each of them, and even comment.
**To be accepted, a comment must be between 1 and 150 characters**.
The first time that a comment is made in the system, a file called **“comments.csv”** that saves the commenting user’s username, the topic’s name, the creator’s username, the content of the comment and the date, is created to save it and all of the future comments.

### How exploring works

When the user explores the system, all the topics stored will be printed, and if he decides to enter any of them, every comment related to it will be displayed.
If he doesn’t want to enter a topic or (once inside a topic) comment on a topic, he just has to type the word “exit”, and the menu will be displayed again.

### Logging out and exiting the system

One of the options allows the user to **log out**, going back to the original menu that has three options (login, register and exit).
Also, there is an option to **exit**, which will do the same as the one in the first menu (exit the program with a message).

Those are the general actions that a user can experience in this program, all being managed by one or more functions.
