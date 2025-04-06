import math

class Category:

    # Init creating the ledger list and the name
    def __init__(self, name):
        self.name = name
        self.ledger = []

    # Create the print format
    def __str__(self):
        title = f"{self.name:*^30}"
        ledger_lines = []

        # For loop to get every entry in ledger
        for entry in self.ledger:

            # Description should be max 23 characters long
            description = entry['description'][:23]
            amount = f"{entry['amount']:.2f}"
            # Confusing part, since the title needs exactly 30 characters, giving the description a padding of 23 and amount a padding of 7
            ledger_lines.append(f"{description:<23}{amount:>7}")
        
        total = f"Total: {self.get_balance():.2f}"
        return '\n'.join([title] + ledger_lines + [total])

    # Takes an amount and appends it to the ledger
    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    # Takes an amount previously depositted
    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    # Gets the total balance after subtracting the deposits with the withdraws
    def get_balance(self):
        return sum(entry['amount'] for entry in self.ledger)
        
    # Transfer a given amount from a category to another
    def transfer(self, amount, destination):
        if self.check_funds(amount):
            self.withdraw(amount, description=f'Transfer to {destination.name}')
            destination.deposit(amount, description=f'Transfer from {self.name}')
            return True
        return False

    # Checks if the funds trying to be used are higher than the total funds stored
    def check_funds(self, amount):
        funds = self.get_balance()

        if amount > funds:
            return False
        return True

def create_spend_chart(categories):
    # Title
    header = "Percentage spent by category\n"
    chart = ""

    # Finding the total spent using a for loop
    total_spent = sum(
        abs(entry['amount'])
        for category in categories
        for entry in category.ledger
        if entry['amount'] < 0
    )
    percentages = []

    # Finding the percentage for each category and rounding to nearest 10
    for category in categories:
        spent = sum(abs(entry['amount']) for entry in category.ledger if entry['amount'] < 0)
        percentage = int((spent / total_spent) * 100)
        percentage = round(percentage // 10) * 10
        percentages.append(percentage)  # Round down to nearest 10
    # Creating the range, 100, -1 going backwards one step, -10 subtracting 10 every step
    for i in range(100, -1, -10):
        chart += f"{i:3}| "
        for percentage in percentages:
            chart += "o" if percentage >= i else " "
            chart += "  "
        chart += "\n"

    # Bottom line
    chart += "    " + "-" * (3 * len(categories) + 1) + "\n"

    # Printing category names vertically

    # Getting names and the length of the longest name
    names = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda name: len(name), names))

    # This part is what gives padding to the names
    padded_names = list(map(lambda name: name.ljust(max_length), names))

    # Create vertical columns for each name
    for i in range(max_length):
        chart += "     "
        for name in padded_names:
            chart += name[i] + "  "
        chart += "\n"
        

    return (header + chart).rstrip('\n')
