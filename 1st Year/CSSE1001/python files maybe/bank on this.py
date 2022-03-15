"""Simple Banking Simulation"""

savings_account = 10000
high_interest_account = 100000

more_transactions = True

client_id = input("Please enter your client id: ")
client_password = input("Please enter your password: ")


if client_id == "123" and client_password == "abc" :
    while more_transactions :
        print("Select the transaction you wish to perform")
        print("1) Check all balances")
        print("2) Transfer money between accounts")
        print("3) Pay a BPay bill")
        print("Q) Quit")
        selection = input("Please enter your selection: ")

        if selection == "1" :
            print("Balance of savings account is $", savings_account/100, sep='')
            print("Balance of high interest account is $",
                  high_interest_account/100, sep='')
        elif selection == "2" :
            from_account = input("Select amount to transfer from: (1) or (2)" )
            to_account = input("Select amount to transfer to: (1) or (2)" )
            transfer_amount = input("Enter the amount to transfer: ")
            if from_account == "1" :
                savings_account -= int(transfer_amount)
                high_interest_account += int(transfer_amount)
                print("The balance of the savings account is now $",
                      savings_account/100, sep='')
                print("The balance of the high interest acoount is now $",
                      high_interest_account/100, sep='')
            else :
                savings_account += transfer_amount
                high_interest_account -= transfer_amount
                print("The balance of the savings account is now $",
                      savings_account/100, sep='')
                print("The balance of the high interest acoount is now $",
                      high_interest_account/100, sep='')
                
            

            
