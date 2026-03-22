import unittest
from accounts import Account


class TestAccountInitialization(unittest.TestCase):
    """Test cases for Account initialization."""
    
    def test_initialize_with_positive_balance(self):
        """Test initialization with a positive balance."""
        account = Account(100.0)
        self.assertEqual(account.balance, 100.0)
    
    def test_initialize_with_zero_balance(self):
        """Test initialization with zero balance."""
        account = Account(0.0)
        self.assertEqual(account.balance, 0.0)
    
    def test_initialize_with_negative_balance_raises_error(self):
        """Test that initialization with negative balance raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Account(-50.0)
        self.assertEqual(str(context.exception), "Initial balance must be non-negative.")
    
    def test_initialize_with_large_balance(self):
        """Test initialization with a large balance."""
        account = Account(1000000.50)
        self.assertEqual(account.balance, 1000000.50)
    
    def test_initialize_with_small_decimal_balance(self):
        """Test initialization with a small decimal balance."""
        account = Account(0.01)
        self.assertEqual(account.balance, 0.01)


class TestAccountDeposit(unittest.TestCase):
    """Test cases for Account deposit method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.account = Account(100.0)
    
    def test_deposit_positive_amount(self):
        """Test depositing a positive amount."""
        self.account.deposit(50.0)
        self.assertEqual(self.account.balance, 150.0)
    
    def test_deposit_zero_amount(self):
        """Test depositing zero amount."""
        self.account.deposit(0.0)
        self.assertEqual(self.account.balance, 100.0)
    
    def test_deposit_negative_amount_raises_error(self):
        """Test that depositing a negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-25.0)
        self.assertEqual(str(context.exception), "Deposit amount must be non-negative.")
    
    def test_deposit_multiple_times(self):
        """Test multiple consecutive deposits."""
        self.account.deposit(50.0)
        self.account.deposit(25.0)
        self.account.deposit(10.0)
        self.assertEqual(self.account.balance, 185.0)
    
    def test_deposit_large_amount(self):
        """Test depositing a large amount."""
        self.account.deposit(999999.99)
        self.assertEqual(self.account.balance, 1000099.99)
    
    def test_deposit_decimal_amount(self):
        """Test depositing a decimal amount."""
        self.account.deposit(12.50)
        self.assertEqual(self.account.balance, 112.50)
    
    def test_deposit_returns_none(self):
        """Test that deposit returns None."""
        result = self.account.deposit(50.0)
        self.assertIsNone(result)


class TestAccountWithdraw(unittest.TestCase):
    """Test cases for Account withdraw method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.account = Account(100.0)
    
    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount."""
        result = self.account.withdraw(30.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 70.0)
    
    def test_withdraw_entire_balance(self):
        """Test withdrawing the entire balance."""
        result = self.account.withdraw(100.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 0.0)
    
    def test_withdraw_more_than_balance(self):
        """Test withdrawing more than available balance."""
        result = self.account.withdraw(150.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 100.0)
    
    def test_withdraw_zero_amount(self):
        """Test withdrawing zero amount."""
        result = self.account.withdraw(0.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 100.0)
    
    def test_withdraw_negative_amount_raises_error(self):
        """Test that withdrawing a negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-25.0)
        self.assertEqual(str(context.exception), "Withdrawal amount must be non-negative.")
    
    def test_withdraw_from_zero_balance(self):
        """Test withdrawing from a zero balance account."""
        account = Account(0.0)
        result = account.withdraw(10.0)
        self.assertFalse(result)
        self.assertEqual(account.balance, 0.0)
    
    def test_withdraw_multiple_times(self):
        """Test multiple consecutive withdrawals."""
        result1 = self.account.withdraw(20.0)
        result2 = self.account.withdraw(30.0)
        result3 = self.account.withdraw(25.0)
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)
        self.assertEqual(self.account.balance, 25.0)
    
    def test_withdraw_decimal_amount(self):
        """Test withdrawing a decimal amount."""
        result = self.account.withdraw(12.50)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 87.50)
    
    def test_withdraw_just_over_balance(self):
        """Test withdrawing just over the available balance."""
        result = self.account.withdraw(100.01)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 100.0)
    
    def test_withdraw_large_amount(self):
        """Test attempting to withdraw a large amount."""
        result = self.account.withdraw(999999.99)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 100.0)


class TestAccountGetBalance(unittest.TestCase):
    """Test cases for Account get_balance method."""
    
    def test_get_balance_initial(self):
        """Test getting balance after initialization."""
        account = Account(100.0)
        self.assertEqual(account.get_balance(), 100.0)
    
    def test_get_balance_after_deposit(self):
        """Test getting balance after a deposit."""
        account = Account(100.0)
        account.deposit(50.0)
        self.assertEqual(account.get_balance(), 150.0)
    
    def test_get_balance_after_withdrawal(self):
        """Test getting balance after a withdrawal."""
        account = Account(100.0)
        account.withdraw(30.0)
        self.assertEqual(account.get_balance(), 70.0)
    
    def test_get_balance_returns_float(self):
        """Test that get_balance returns a float."""
        account = Account(100)
        result = account.get_balance()
        self.assertIsInstance(result, float)
    
    def test_get_balance_zero(self):
        """Test getting balance when it's zero."""
        account = Account(0.0)
        self.assertEqual(account.get_balance(), 0.0)


class TestAccountIntegration(unittest.TestCase):
    """Integration tests for Account operations."""
    
    def test_deposit_and_withdraw_sequence(self):
        """Test a sequence of deposits and withdrawals."""
        account = Account(100.0)
        account.deposit(50.0)
        self.assertEqual(account.get_balance(), 150.0)
        account.withdraw(30.0)
        self.assertEqual(account.get_balance(), 120.0)
        account.deposit(80.0)
        self.assertEqual(account.get_balance(), 200.0)
        result = account.withdraw(200.0)
        self.assertTrue(result)
        self.assertEqual(account.get_balance(), 0.0)
    
    def test_failed_withdrawal_does_not_affect_balance(self):
        """Test that failed withdrawal does not affect balance."""
        account = Account(50.0)
        result = account.withdraw(100.0)
        self.assertFalse(result)
        self.assertEqual(account.get_balance(), 50.0)
    
    def test_complex_transaction_sequence(self):
        """Test a complex sequence of transactions."""
        account = Account(500.0)
        account.deposit(200.0)
        account.withdraw(150.0)
        account.deposit(75.0)
        account.withdraw(200.0)
        account.deposit(100.0)
        self.assertEqual(account.get_balance(), 525.0)
    
    def test_error_during_sequence_does_not_affect_previous_balance(self):
        """Test that an error during sequence doesn't affect previous operations."""
        account = Account(100.0)
        account.deposit(50.0)
        try:
            account.deposit(-10.0)
        except ValueError:
            pass
        self.assertEqual(account.get_balance(), 150.0)


class TestAccountEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_very_small_deposit(self):
        """Test depositing a very small amount."""
        account = Account(0.0)
        account.deposit(0.001)
        self.assertAlmostEqual(account.get_balance(), 0.001, places=3)
    
    def test_very_small_withdrawal(self):
        """Test withdrawing a very small amount."""
        account = Account(1.0)
        result = account.withdraw(0.001)
        self.assertTrue(result)
        self.assertAlmostEqual(account.get_balance(), 0.999, places=3)
    
    def test_floating_point_precision(self):
        """Test handling of floating point precision issues."""
        account = Account(0.1)
        account.deposit(0.2)
        self.assertAlmostEqual(account.get_balance(), 0.3, places=10)
    
    def test_large_number_of_operations(self):
        """Test account with large number of operations."""
        account = Account(1000.0)
        for _ in range(100):
            account.deposit(1.0)
        for _ in range(50):
            account.withdraw(1.0)
        self.assertEqual(account.get_balance(), 1050.0)


if __name__ == '__main__':
    unittest.main()