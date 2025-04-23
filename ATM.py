import csv
import random

# Dictionary to store accounts
accounts = {}
atm_cash = 100000  # Total cash available in the ATM

# Load account data from data.csv
def load_accounts():
    try:
        with open('data.csv', 'r') as file:
            for line in file:
                token, pin, balance = line.strip().split(';')
                accounts[int(token)] = [int(pin), int(balance)]
    except FileNotFoundError:
        print("No account data found. Starting with empty accounts.")

# Save account data to data.csv
def save_accounts():
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for token, (pin, balance) in accounts.items():
            writer.writerow([token, pin, balance])

# Log a transaction to history.csv
def log_transaction(token, pin, amount, action):
    with open('history.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([token, pin, amount, action])

# Create a new account with a random token and pin
def create_account(initial_deposit):
    while True:
        token = random.randint(10000, 99999)
        if token not in accounts:
            break
    pin = random.randint(100, 999)
    accounts[token] = [pin, initial_deposit]
    save_accounts()
    print(f"Account created successfully!\nToken: {token}, PIN: {pin}")

# Check if token and pin are correct
def authorize(token, pin):
    if token in accounts and accounts[token][0] == pin:
        return True 
    print("Access Denied.")
    return False

# Deposit money to an account
def deposit(token, pin, amount):
    if authorize(token, pin):
        accounts[token][1] += amount
        save_accounts()
        log_transaction(token, pin, amount, "DEPOSIT")
        print("Deposit successful!")

# Withdraw money from an account
def withdraw(token, pin, amount):
    global atm_cash
    if authorize(token, pin):
        if amount > 20000:
            print("Cannot withdraw more than 20000 at once.")
            return
        if accounts[token][1] >= amount and atm_cash >= amount:
            accounts[token][1] -= amount
            atm_cash -= amount
            save_accounts()
            log_transaction(token, pin, amount, "WITHDRAW")
            print("Withdrawal successful!")
        else:
            print("Insufficient balance or ATM cash.")

# Show transaction history for a user
def show_history(token, pin):
    if authorize(token, pin):
        try:
            with open('history.csv', 'r') as file:
                for line in file:
                    t, p, amt, action = line.strip().split(';')
                    if int(t) == token:
                        print(f"{action}: ₦{amt}")
        except FileNotFoundError:
            print("No transaction history found.")



def main():
    load_accounts()
    while True:
        print("\n====== ATM MENU ======")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Show Transaction History")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            initial_deposit = int(input("Enter initial deposit amount: "))
            create_account(initial_deposit)

        elif choice == "2":
            token = int(input("Enter your token: "))
            pin = int(input("Enter your PIN: "))
            amount = int(input("Enter amount to deposit: "))
            deposit(token, pin, amount)

        elif choice == "3":
            token = int(input("Enter your token: "))
            pin = int(input("Enter your PIN: "))
            amount = int(input("Enter amount to withdraw: "))
            withdraw(token, pin, amount)

        elif choice == "4":
            token = int(input("Enter your token: "))
            pin = int(input("Enter your PIN: "))
            show_history(token, pin)

        elif choice == "5":
            print("Thank you for using the ATM!")
            break

        else:
            print("Invalid choice. Please try again.")

#calling main function 
main()
