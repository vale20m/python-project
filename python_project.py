import os
import sys
import csv
import re
import datetime



# I developed a class Account to manage everything related to username and password.

class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username
    
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password



# Main function of the file.

def main():
    os.system("cls")
    user_account = automatic_login()
    while True:
        user_account = get_last_user()
        manage_user_action(user_account)



# Functions related to menus and navigation

# manage_start_option() is the starter function of the program. It promps the user with some options, and depending on the user's choice, it does something different.
# If the user enters '1' or '2', it returns the input, and if the user enters '3', it exits the program. However, it promps the user again in any other case.

def manage_start_option():
    print("Welcome to Valentin's comments system!")
    while True:
        option = input("Choose one of these options:\n1 --> Login (if you already have an account)\n2 --> Register (if you don't have an account)\n3 --> Exit from the system\nOption: ").strip()
        os.system("cls")
        match option:
            case '1' | '2':
                return option
            case '3':
                sys.exit("Have a nice day!")
            case _:
                print("Please enter a valid option (1, 2 or 3)")

# choose_start_option(option) receives the option entered by the user and calls a different function depending on it.
# If the option is '1', it calls the function login_user() and if it is '2', register_user() is called instead.

def choose_start_option(option):
    if option == '1':
        return login_user()
    else:
        return register_user()

# manage_user_action(account) prompts the user with a variety of options (when it has logged in), including creating a topic to discuss, commenting on a topic, logging out and exiting from the system.
        
def manage_user_action(account):
    print(f"Welcome to the system, {account.username}!")
    while True:
        option = input("Choose among the following options:\n1 --> Explore and comment on a topic of your choice\n2 --> Create a new topic to discuss\n3 --> Log out (to switch to another account)\n4 --> Exit from the system\nOption: ").strip()
        match option:
            case '1' | '2' | '3':
                return choose_user_action(account, option)
            case '4':
                os.system("cls")
                sys.exit(f"Have a nice day, {account.username}!")
            case _:
                os.system("cls")
                print("Please, enter a valid argument (1, 2, 3 or 4)")

# choose_user_action(account, option) calls a different function depending on the user's choice

def choose_user_action(account, option):
    if option == '1':
        return comment_topic(account)
    elif option == '2':
        return create_topic(account)
    else:
        os.system("cls")
        os.remove('last_user.csv')
        return choose_start_option(manage_start_option())



# Functions related to register an acconut and login into the system, among checking different things

# register_user() asks the user for a username and a password to create a new account in users.csv.
# Then it validates the password entered and checks that the username has not been taken already (if there is another user with the same usename).
# It that action raises an error (because the file does not exists, then another function creates it and tries again).
# If the username is valid, then the account is added to the file users.csv.

def register_user():
    new_account = Account(input("Choose a username: "), input("Choose a password: "))
    retry_password(new_account)
    while True:
        try:
            check_username_in_users(new_account)
            os.system("cls")
            return choose_start_option(manage_start_option())
        except FileNotFoundError:
            create_users_file()

# check_username_in_users(account) checks that there is no account that has the same name that the user entered.
# If there is, prompts the user again, otherwise it will add the account to the file.

def check_username_in_users(account):
    users = search_users()
    while True:
        os.system("cls")
        retry_username(account)
        if account.username in users:
            os.system("cls")
            account.username = input("That username is already taken. Please enter another one: ")
        else:
            create_account(account)
            return
        
# create_account(account) adds an account to the users.csv file.

def create_account(account):
    with open("users.csv", 'a', newline="") as file:
        headers = ["username", "password"]
        writer = csv.DictWriter(file, fieldnames = headers)
        writer.writerow({"username": account.username, "password": account.password})

# login_user() first checks that there are any users created, and if there are it continues to ask for the user for their username and password.
# Then, it checks that the user's username is part of a created account (in users.csv) to finaly validate the password that the user entered (if it is correct, it returns the account).

def login_user():
    try:
        users = search_users()
        if len(users) == 0:
            print("Error: There are no users registered in the system")
            return choose_start_option(manage_start_option())
        login_account = Account(input("Enter your username: "), input("Enter your password: "))
        if login_account.username not in users:
            os.system("cls")
            print("Error: That username does not exists in the system")
            return choose_start_option(manage_start_option())
        return try_password_again(login_account)
    except FileNotFoundError:
        os.system("cls")
        print("Error: There are no accounts created yet")
        return choose_start_option(manage_start_option())

# search_users() returns a list with all of the usernames saved in users.csv.

def search_users():
    with open("users.csv", 'r') as file:
        reader = csv.DictReader(file)
        users = []
        for row in reader:
            users.append(row["username"])
        return users

# try_password_again(account) checks that the password associated to an account is equal to the password entered by the user, and if its not, it gives the user.
# two more tries to enter it correctly. If the user fails, an error message is displayed and the start function is called, otherwise, the account is returned.

def try_password_again(account):
    correct_password = return_correct_password(account)
    count = 3
    while correct_password != account.password:
        if count > 1:
            count -= 1
            os.system("cls")
            print("Error: Incorrect password")
            account.password = input(f"Please enter your password again (opportunities left: {count}): ")
        else:
            os.system("cls")
            print("Error: Login failed, you entered an incorrect password three times")
            return choose_start_option(manage_start_option())
    os.system("cls")
    create_last_user_file(account)
    return account



# Functions related to saving the last user account and using it

# automatic_login() tries to return the last user that logged in the system, but if it is not storaged, it prompts the user with the starting menu (login, register or exit).

def automatic_login():
    try:
        return get_last_user()
    except FileNotFoundError:
        return choose_start_option(manage_start_option())

# get_last_user() returns the user storaged in last_user.csv

def get_last_user():
    with open("last_user.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            account = Account(row["username"], row["password"])
        return account



# return_correct_password(account) searches for the user's entered username in users.csv, and when it founds it, returns the password associated to it.

def return_correct_password(account):
    with open("users.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if account.username == row["username"]:
                return row["password"]



# Functions related to creating topics and making comments

# create_topic(account) creates a topic with a name entered by the user (he cannot have two topics with the same name), saving it with the actual date.
# If topics.csv does not exist, call another function to create it.

def create_topic(account):
    os.system("cls")
    topic = input("Enter a name for your topic: ").strip()
    topic = retry_topic_name(topic)
    while True:
        try:
            os.system("cls")
            if check_topic_name_by_user(account, topic):
                print("Error: You have already created a topic with the exact same name")
                return manage_user_action(account)
            save_topic(account, topic)
            print("Topic created successfully!")
            return manage_user_action(account)
        except FileNotFoundError:
            create_topics_file()

# check_topic_name_by_user(account, topic) returns True if there is already a topic with that name created by the same user in topics.csv, and False otherwise.

def check_topic_name_by_user(account, topic):
    with open ("topics.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == account.username and row["topic"] == topic:
                return True
        return False

# save_topic(account, topic) saves the topic in topics.csv with the username, topic's name and actual date.
    
def save_topic(account, topic):
    with open("topics.csv", 'a', newline="") as file:
        headers = ["username", "topic", "date"]
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerow({"username": account.username, "topic": topic, "date": datetime.date.today()})

# comment_topic(account) creates a comment in a specified topic with a content entered by the user, saving it with the actual date and the name of the topic.
# If topics.csv does not exist, call another function to create it.

def comment_topic(account):
    try:
        topics_list = get_topics()
        os.system("cls")
        print("Choose one of the avaliable topics from below:\n")
        print_topics(account, topics_list)
        topic_num = manage_topic_input(account, topics_list)
        if topic_num == None:
            return account
        chosen_topic_name = topics_list[topic_num]["topic"]
        chosen_topic_creator_username = topics_list[topic_num]["username"]
        while True:
            try:
                print_comments(account, get_comments(chosen_topic_name, chosen_topic_creator_username))
                return manage_comment_input(account, chosen_topic_name, chosen_topic_creator_username)
            except FileNotFoundError:
                create_comments_file()
    except FileNotFoundError:
        os.system("cls")
        print("Error: There are no topics in the system yet")
        return manage_user_action(account)
    
# get_topics() returns a list with all the elements stored in topics.csv.

def get_topics():
    with open("topics.csv", 'r') as file:
        reader = csv.DictReader(file)
        topics_list = []
        for row in reader:
            topics_list.append({"username": row["username"], "topic": row["topic"], "date": row["date"]})
        return topics_list

# print_topics(list) prints all the topics saved in topics.csv.

def print_topics(account, list):
    if len(list) > 0:
        for count, item in enumerate(list):
            print(f"{count+1} - {item["topic"]}\nCreated by {item["username"]}, on {item["date"]}\n")
    else:
        print("Error: There are no topics created in the system yet")
        manage_user_action(account)

# manage_topic_input(account, list) manage the input of the user when he wants to choose a topic of the list shown.
# If the user enters a number out of range or enters anything else but a number, a message in printed instead.

def manage_topic_input(account, list):
    while True:
        try:
            n = input("Option (number, type 'exit' (without the quotation marks) if you want to go back): ").strip()
            n = int(n)-1
            if 0 <= n < len(list):
                os.system("cls")
                return n
            else:
                print(f"Error: The topic you specified does not exist (there is not a topic {n+1}). Please try again below")
        except ValueError:
            if n.lower() == "exit":
                os.system("cls")
                manage_user_action(account)
                return None
            else:
                print("Error: A integer was expected, but you entered something else (a string). Please try again below")

# manage_comment_input(account, topic) ensures that the comment entered by the user is valid, and if it is, it saves the comment in comments.csv.
# If the users enters the word 'exit', the program prompts the action menu back and does not saves anything.

def manage_comment_input(account, topic, username):
    text = input("What are your thoughts on this topic? (type 'exit' (without the quotation marks) if you want to fo back)\n").strip()
    os.system("cls")
    text = retry_comment(text)
    os.system("cls")
    if text.lower() == "exit":
        return manage_user_action(account)
    else:
        save_comment(account, topic, username, text)
        
# get_comments(topic) returns a list with all the comments made in a specified topic (saved in comments.csv).

def get_comments(topic, username):
    with open("comments.csv", 'r') as file:
        reader = csv.DictReader(file)
        topic_comments = []
        for row in reader:
            if topic == row["topic"] and username == row["creator_username"]:
                topic_comments.append({"username": row["username"], "comment": row["comment"], "date": row["date"]})
        return topic_comments

# print_comments(account, list) prints all the comments made in an specified topic. If there aren't any comments, it prints a message instead.

def print_comments(account, list):
    if len(list) > 0:
        os.system("cls")
        print(f"Comments ({len(list)}):\n")
        for item in list:
            print(f"{item["username"]} on {item["date"]} commented:\n{item["comment"]}\n")
    else:
        print("This topic has not been commented yet. Be the first one!")

# save_comment(account, topic, comment) saves a comment made by an user specifying its username, the topic name, the content of the comment and the actual date.

def save_comment(account, topic, username, comment):
    with open("comments.csv", 'a', newline="") as file:
        headers = ["username", "topic", "creator_username", "comment", "date"]
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerow({"username": account.username, "topic": topic, "creator_username": username, "comment": comment, "date": datetime.date.today()})



# Functions that create different files in the system

# create_users_file() creates the file "users.csv" with the fieldnames "username" and "password", if it does not exists in the system.
# This file stores the accounts registered in the system.

def create_users_file():
    with open("users.csv", 'w', newline="") as file:
        headers = ["username", "password"]
        writer = csv.DictWriter(file, fieldnames = headers)
        writer.writeheader()
        print("Account created successfully!")

# create_last_user_file(account) creates a file called "last_user.csv", which stores the last user that logged in the system with the fieldnames "username" and "password".
# This file stores the last user that logged in the system.

def create_last_user_file(account):
    with open("last_user.csv", 'w', newline='') as file:
        headers = ["username", "password"]
        writer = csv.DictWriter(file, fieldnames = headers)
        writer.writeheader()
        writer.writerow({"username": account.username, "password": account.password})

# create_topics_file() creates the file "topics.csv" with the fieldnames "username", "topic" and "date", in case it does not exists in the system.
# This file stores the topics created in the system.

def create_topics_file():
    with open("topics.csv", 'w', newline='') as file:
        headers = ["username", "topic", "date"]
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

# create_comments_file() create the file "comments.csv" with the fieldnames "username", "topic", "creator_username", "comment" and "date", in case it does not exist in the system
# This file stores the comments related to topics in the system.

def create_comments_file():
    with open("comments.csv", 'w', newline='') as file:
        headers = ["username", "topic", "creator_username", "comment", "date"]
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()



# Functions that validate different inputs

# retry_password(account) validates the password given by the user, which must contain at least 6 characters and cannot include quotation marks nor spaces.
# If the pasword is incorrect, the function prompts the user again.

def validate_password_re(account):
    return re.search(r"^([^\s\'\"]{6,})$", account.password)

def retry_password(account):
    while not validate_password_re(account):
        os.system("cls")
        print ("Invalid password\nIt must contain at least 6 characters (which cannot include quotation marks nor spaces)")
        account.password = input("Please enter another password: ")

# retry_username(account) validates the username given by the user, which must contain between 4 and 15 characters (only letters, numbers and underscores)
# If the username is incorrect, the function prompts the user again.

def validate_username_re(account):
    return re.search(r"^([\w]{4,15})$", account.username)

def retry_username(account):
    while not validate_username_re(account):
        os.system("cls")
        print ("Invalid username\nIt must contain between 4 and 15 characters (which can only be letters, numbers and underscores)")
        account.username = input("Please enter another username: ")

# retry_topic_name(topic) validates the name entered to create a topic in the system, which must contain between 10 and 50 characters.
# If the topic name is incorrect, the function prompts the user again.

def validate_topic_name(topic):
    return re.search(r"^(.{10,50})$", topic)

def retry_topic_name(topic):
    while not validate_topic_name(topic):
        os.system("cls")
        print ("Error: Invalid topic name\nIt must contain between 10 and 50 characters")
        topic = input("Please enter another topic name: ").strip()
    return topic

# retry_comment(comment) validates the comment entered to create a comment related to a topic in the system, which must contain between 1 and 150 characters.
# If the comment is incorrect, the function prompts the user again.

def validate_comment(comment):
    return re.search(r"^(.{1,150})$", comment)

def retry_comment(comment):
    while not validate_comment(comment):
        os.system("cls")
        print ("Invalid comment\nIt must contain between 1 and 150 characters")
        comment = input("Please enter another comment (type 'exit' (without the quotation marks) if you want to fo back)\n").strip()
    return comment

if __name__ == "__main__":
    main()