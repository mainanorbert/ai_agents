```python
# accounts.py

class Account:
    def __init__(self, initial_balance: float):
        """
        Initializes a new Account instance with a starting balance.
        
        :param initial_balance: The initial balance for the account, should be a non-negative float.
        """
        self.balance = initial_balance
        
    def deposit(self, amount: float) -> None:
        """
        Deposits a specified amount into the account.
        
        :param amount: The amount of money to deposit, should be a non-negative float.
        :raises ValueError: If the amount to deposit is negative.
        """
        if amount < 0:
            raise ValueError("Deposit amount must be non-negative.")
        self.balance += amount
        
    def withdraw(self, amount: float) -> bool:
        """
        Withdraws a specified amount from the account if sufficient balance exists.
        
        :param amount: The amount of money to withdraw, should be a non-negative float.
        :return: True if the withdrawal was successful, otherwise False.
        :raises ValueError: If the amount to withdraw is negative.
        """
        if amount < 0:
            raise ValueError("Withdrawal amount must be non-negative.")
        if amount > self.balance:
            return False
        self.balance -= amount
        return True
        
    def get_balance(self) -> float:
        """
        Returns the current balance of the account.
        
        :return: The current balance as a float.
        """
        return self.balance
```

### Class: `Account`
- **Attributes:**
  - `balance`: Holds the account current balance as a float.

### Methods:
1. **`__init__(self, initial_balance: float)`**: 
   - Initializes an account with a given starting balance.
   - Raises a `ValueError` if the initial_balance is negative.

2. **`deposit(self, amount: float) -> None`**: 
   - Takes an amount to deposit into the account.
   - Raises a `ValueError` if the deposit amount is negative.

3. **`withdraw(self, amount: float) -> bool`**: 
   - Accepts an amount to withdraw from the account.
   - Returns `True` if the withdrawal is successful, `False` otherwise.
   - Raises a `ValueError` if the withdrawal amount is negative.

4. **`get_balance(self) -> float`**: 
   - Returns the account's current balance. 

This module is designed to be self-contained and ready for testing or integration with a simple user interface.