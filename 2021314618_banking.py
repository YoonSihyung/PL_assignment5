import os
import json
import random
from datetime import datetime
import time

def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def isnumber(money):
    try:
        float(money)
        return True
    except ValueError:
        return False

def FirstPage():
    Clear()
    
    print("==== Welcome to PL Banking System ====")
    print("Please login to continue. If you do not registered yet, then register first.")
    
    while True:
        first_input = input("1. login\n2. Register\n3. Exit\n")
        if first_input in ['1', '2', '3']:
            break
        else:
            print("Wrong input. Please input: [1, 2, 3]")
    if first_input == '1':
        Login()
        return
    elif first_input == '2':
        Register()
        return
    else:
        print("Thank you for using PL Banking System!")
        time.sleep(3)
        return


def Login():
    Clear()

    file_path1 = 'users.json'
    if os.path.exists(file_path1):
        with open(file_path1, 'r') as f:
            try:
                users = json.load(f)
                if not users:
                    print("There are no registered users. Please register and be our first customer!")
                    time.sleep(3)
                    FirstPage()
                    return
            except json.JSONDecodeError:
                print("There are no registered users. Please register and be our first customer!")
                time.sleep(3)
                FirstPage()
                return
    else:
        print("There are no registered users. Please register and be our first customer!")
        time.sleep(3)
        FirstPage()
        return
    
    print("Enter username and password to use the system.")
    
    while True:
        login_username = input("Username: ")
        login_password = input("Password: ")
        
        if any(user['username'] == login_username and user['password'] == login_password for user in users):
            break
        else:
            print("Wrong username or password. Please try again.")
    
    Logined(login_username)
    return

def Logined(username):
    Clear()
    
    print(f"==== Welcome {username} ====")

    file_path1 = 'users.json'
    if os.path.exists(file_path1) and os.path.getsize(file_path1) > 0:
        with open(file_path1, 'r') as f:
            users = json.load(f)
    else:
        users = []
    
    user = None
    for i in users:
        if i['username'] == username:
            user = i
            break

    print("==== Your Account Info ====")
    print(f"Username: {user['username']}")
    print(f"Account Number: {user['account_number']}")
    print(f"Current Balance: ${user['balance']}")

    print("==== Select Option ====")
    while True:
        option_input = input("1. Check History\n2. Withdraw Money\n3. Deposit Money\n4. Transfer Money\n5. Logout\n")
        if option_input not in ['1', '2', '3', '4', '5']:
            print("Wrong input. Please input: [1, 2, 3, 4, 5]")
        else:
            break
    
    if option_input == '1':
        CheckHistory(user['username'])
        return
    elif option_input == '2':
        Withdraw(user['username'])
        return
    elif option_input == '3':
        Deposit(user['username'])
        return
    elif option_input == '4':
        Transfer(user['username'])
        return
    else:
        Logout()
        return

def CheckHistory(username):
    Clear()

    print(f"Transaction History for {username}")
    print("--------------------------------------------------")
    
    file_path2 = 'transactions.json'
    if os.path.exists(file_path2) and os.path.getsize(file_path2) > 0:
        with open(file_path2, 'r') as f:
            transactions = json.load(f)
    else:
        transactions = []
    
    check = 0
    for i in range(len(transactions)-1, -1, -1):
        transaction = transactions[i]
        if transaction['type'] == 'Transfer':
            if transaction['from'] == username or transaction['to'] == username:
                check = 1
                print(f"Time: {transaction['time']}")
                print(f"Transaction Type: {transaction['type']}")
                print(f"From: {transaction['from']}")
                print(f"To: {transaction['to']}")
                print(f"Amount: ${float(transaction['amount'])}")
                print("--------------------------------------------------")
        else:
            if transaction['username'] == username:
                check = 1
                print(f"Time: {transaction['time']}")
                print(f"Transaction Type: {transaction['type']}")
                print(f"Account: {transaction['username']}")
                print(f"Amount: ${float(transaction['amount'])}")
                print("--------------------------------------------------")
    
    if not check:
        print("You have no history yet.")
        print("--------------------------------------------------")
    
    while True:
        ret = input("Press Enter to return to main screen.")
        if ret == '':
            Logined(username)
            return
        else:
            print("Please press Enter to return to main screen.")


def Withdraw(username):
    Clear()
    
    file_path1 = 'users.json'
    if os.path.exists(file_path1) and os.path.getsize(file_path1) > 0:
        with open(file_path1, 'r') as f:
            users = json.load(f)
    else:
        users = []
    
    user = None
    for i in users:
        if i['username'] == username:
            user = i
            break
    
    print("==== Your Account Info ====")
    print(f"Username: {user['username']}")
    print(f"Account Number: {user['account_number']}")
    print(f"Current Balance: ${user['balance']}")
    
    while True:
        money = input("Enter the amount you want to withdraw: ")
        if isnumber(money) and float(money) <= user['balance']:
            money = float(money)
            break
        else:
            if float(money) > user['balance']:
                print(f"Please input less than {user['balance']}.")
            else:
                print("Wrong input.")
    
    while True:
        pin_try = input("Enter your PIN to confirm the withdrawl: ")
        if pin_try == user['pin']:
            break
        else:
            print("Wrong PIN. Please try again.")
    
    while True:
        ensure = input(f"Are you sure for withdrawing ${money}? [Y/N] : ")
        if ensure not in ['Y', 'N']:
            print("Wrong input. Please input [Y/N]")
        else:
            break
    
    if ensure == 'Y':
        user['balance'] -= money

        with open(file_path1, 'w') as f:
            json.dump(users, f, indent = 4)
        
        file_path2 = 'transactions.json'
        if os.path.exists(file_path2) and os.path.getsize(file_path2) > 0:
            with open(file_path2, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        history.append({'type': 'Withdraw', 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'username': user['username'], 'amount': money})

        with open(file_path2, 'w') as f:
            json.dump(history, f, indent = 4)

        print(f"Withdraw ${money} is completed. Your new balance is ${user['balance']}.")
        while True:
            ret = input("Press Enter to return to main screen.")
            if ret == '':
                Logined(user['username'])
                return
            else:
                print("Please press Enter to return to main screen.")
    
    else:
        print("Withdrawl cancelled.")
        while True:
            ret = input("Press Enter to return to main screen.")
            if ret == '':
                Logined(user['username'])
                return
            else:
                print("Please press Enter to return to main screen.")
    


def Deposit(username):
    Clear()

    file_path1 = 'users.json'
    if os.path.exists(file_path1) and os.path.getsize(file_path1) > 0:
        with open(file_path1, 'r') as f:
            users = json.load(f)
    else:
        users = []
    
    user = None
    for i in users:
        if i['username'] == username:
            user = i
            break
    
    print("==== Your Account Info ====")
    print(f"Username: {user['username']}")
    print(f"Account Number: {user['account_number']}")
    print(f"Current Balance: ${user['balance']}")

    while True:
        money = input("Enter the amount you want to deposit: ")
        if isnumber(money):
            money = float(money)
            break
        else:
            print("Wrong input.")
    
    while True:
        pin_try = input("Enter your PIN to confirm the deposit: ")
        if pin_try == user['pin']:
            break
        else:
            print("Wrong PIN. Please try again.")
    
    while True:
        ensure = input(f"Are you sure for deposit ${money}? [Y/N] : ")
        if ensure not in ['Y', 'N']:
            print("Wrong input. Please input [Y/N]")
        else:
            break
    
    if ensure == 'Y':
        user['balance'] += money

        with open(file_path1, 'w') as f:
            json.dump(users, f, indent = 4)
        
        file_path2 = 'transactions.json'
        if os.path.exists(file_path2) and os.path.getsize(file_path2) > 0:
            with open(file_path2, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        history.append({'type': 'Deposit', 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'username': user['username'], 'amount': money})

        with open(file_path2, 'w') as f:
            json.dump(history, f, indent = 4)

        print(f"Deposit ${money} is completed. Your new balance is ${user['balance']}.")
        while True:
            ret = input("Press Enter to return to main screen.")
            if ret == '':
                Logined(user['username'])
                return
            else:
                print("Please press Enter to return to main screen.")
    
    else:
        print("Deposit cancelled.")
        while True:
            ret = input("Press Enter to return to main screen.")
            if ret == '':
                Logined(user['username'])
                return
            else:
                print("Please press Enter to return to main screen.")
    

def Transfer(username):
    Clear()

    file_path1 = 'users.json'
    if os.path.exists(file_path1) and os.path.getsize(file_path1) > 0:
        with open(file_path1, 'r') as f:
            users = json.load(f)
    else:
        users = []
    
    user = None
    for i in users:
        if i['username'] == username:
            user = i
            break
    
    print("==== Your Account Info ====")
    print(f"Username: {user['username']}")
    print(f"Account Number: {user['account_number']}")
    print(f"Current Balance: ${user['balance']}")

    while True:
        recipient_number = input("Enter the recipient's account number: ")
        if isnumber(recipient_number) and len(recipient_number) == 5:
            for i in users:
                if i['account_number'] == recipient_number:
                    recipient = i
                    break
            else:
                print("There is no matching account number. Please try again.")
                continue
            break
        else:
            print('Wrong input. Please input five digit number.')
    
    while True:
        money = input("Enter the amount you want to transfer: ")
        if isnumber(money) and float(money) <= user['balance']:
            money = float(money)
            break
        else:
            if float(money) > user['balance']:
                print(f"Please input less than {user['balance']}.")
            else:
                print("Wrong input.")
    
    while True:
        pin_try = input("Enter your PIN to confirm the transfer: ")
        if pin_try == user['pin']:
            break
        else:
            print("Wrong PIN. Please try again.")
    
    while True:
        ensure = input(f"Are you sure for transferring ${money} to {recipient['username']}? [Y/N] : ")
        if ensure not in ['Y', 'N']:
            print("Wrong input. Please input [Y/N]")
        else:
            break
    
    if ensure == 'Y':
        user['balance'] -= money
        recipient['balance'] += money

        with open(file_path1, 'w') as f:
            json.dump(users, f, indent = 4)
        
        file_path2 = 'transactions.json'
        if os.path.exists(file_path2) and os.path.getsize(file_path2) > 0:
            with open(file_path2, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        history.append({'type': 'Transfer', 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'from': user['username'],'to': recipient['username'], 'amount': money})

        with open(file_path2, 'w') as f:
            json.dump(history, f, indent = 4)

        print(f"Transfer ${money} to {recipient['username']} is completed. Your new balance is ${user['balance']}.")
        while True:
            ret = input("Press Enter to return to main screen.")
            if ret == '':
                Logined(user['username'])
                return
            else:
                print("Please press Enter to return to main screen.")
    
    else:
        print("Transfer cancelled.")
        while True:
            ret = input("Press Enter to return to main screen.")
            if ret == '':
                Logined(user['username'])
                return
            else:
                print("Please press Enter to return to main screen.")


def Register():
    Clear()
    
    print("==== Register ====")
    print("Enter username, password and PIN password to register the system.")

    file_path = 'users.json'
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as f:
            users = json.load(f)
    else:
        users = []

    while True:
        username = input("Username: ")
        if any(user['username'] == username for user in users):
            print("Username already exists. Please input another username.")
            print("Register again..")
            print("--------------------------------------------------")
            continue

        password = input("Password: ")
        special_characters = '!@#$%^&*()'
        errors = 0
        if len(password) <= 7:
            print("Password must be over 7 letters.")
            errors = 1
        if not any(i.isupper() for i in password):
            print("Password must contain at least 1 upper letter.")
            errors = 1
        if not any(i in special_characters for i in password):
            print("Password must contain at least 1 special character( !@#$%^&*() ).")
            errors = 1
        
        if errors:
            print("Register again..")
            print("--------------------------------------------------")
            continue

    
        pin = input("PIN: ")
        if not (isnumber(pin) and len(pin) == 4):
            print("Wrong input. Please input four digit number.")
            print("Register again..")
            print("--------------------------------------------------")
            continue

        break
    
    while True:
        num = random.randint(10000, 99999)
        if not any(user.get('user_number') == num for user in users):
            account_number = str(num)
            break

    users.append({'username': username, 'password': password, 'pin': pin, 'account_number': account_number, 'balance': 100.0})

    with open(file_path, 'w') as f:
        json.dump(users, f, indent=4)

    while True:
        ret = input("Register confirmed. Press Enter to return to initial screen.")
        if ret == '':
            FirstPage()
            return
        else:
            print("Please press Enter to return to initial screen.")

def Logout():
    print("Thank you for using PL Banking System!")
    time.sleep(3)
    FirstPage()
    return

FirstPage()