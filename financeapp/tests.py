from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Budget, Account, ZeroBasedCategory, Expense, FiftyThirtyTwentyCategory, Transaction
from django.utils import timezone
import datetime

class FinanceAppTests(TestCase):
  
    #pre Logged in Test
    def test_index_view(self):
        response = self.client.get(reverse('financeapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'financeapp/index.html')
        
    def test_about_view(self):
        response = self.client.get(reverse('financeapp:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'financeapp/about.html')
        
    def test_contact_view(self):
        response = self.client.get(reverse('financeapp:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'financeapp/contact.html')
       
    #Registration and Login Test 
    def setUp(self):
        # Set up a user and log them in
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.budget = Budget.objects.create(user=self.user, budget_name='Test Budget', budget_type='zero_based')
        self.fifty_thirty_twenty_budget = Budget.objects.create(user=self.user, budget_name='Test Fifty Budget', budget_type='fifty_thirty_twenty')
        
        
    #Post Logged in Test for Zero Based Budget
    
    def test_create_budget_page_view(self):
      response = self.client.get(reverse('financeapp:create_budget'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'financeapp/budget.html')
    
    def create_zero_based_budget(self):
      self.assertTrue (Budget.objects.filter(user=self.user, budget_name='Test Budget', budget_type='zero_based').exists())
      
      
      
    #Test for Overview Page
    def test_overview_view(self):
        response = self.client.get(reverse('financeapp:overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'financeapp/overview.html')


   #Test for Help Page
    def test_help_page_view(self):
        response = self.client.get(reverse('financeapp:help'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'financeapp/help_page.html')
        
     #helper function for session
    def set_session(self):
      session = self.client.session
      session['selected_budget_id'] = self.budget.id
      session.save()
    #Test for Accounts
    def test_account_list_view(self):
      self.set_session()

      response = self.client.get(reverse('financeapp:account_list'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'financeapp/accounts.html')
    
    #Test for Add Account
    def test_add_account_view(self): 
      self.set_session()
      
      form_data = {
        'account_name': 'Test Account',
        'account_type': 'CASH',
        'balance': 100
      }
      
      response = self.client.post(reverse('financeapp:add_account'), form_data)
      self.assertEqual(response.status_code, 302)
      self.assertTrue(
        Account.objects.filter(
          account_name='Test Account', 
          balance=100, 
          account_type='CASH', 
          budget=self.budget
          ) .exists() )
      self.assertRedirects(response, reverse('financeapp:account_list'))
      
    #Test for Edit Account
    def test_edit_account_view(self):
      self.set_session()
      
      account = Account.objects.create(account_name='Test Account', account_type='CASH', balance=100, budget=self.budget)
      
      form_data = {
        'account_id': account.id,
        'account_name': 'Test Account',
        'account_type': 'CASH',
        'balance': 200
      }
      
      response = self.client.post(reverse('financeapp:edit_account'), form_data)
      self.assertEqual(response.status_code, 302)
      self.assertTrue(Account.objects.filter(account_name='Test Account', balance=200, account_type='CASH', budget=self.budget).exists())
      self.assertRedirects(response, reverse('financeapp:account_list'))
      
    #Test for Delete Account
    def test_delete_account_view(self):
      self.set_session()
      
      account = Account.objects.create(account_name='Delete Account', account_type='CASH', balance=100, budget=self.budget)
      
      response = self.client.post(reverse('financeapp:delete_account', args=[account.id]))
      self.assertEqual(response.status_code, 302)
     
      self.assertFalse(Account.objects.filter(account_name='Delete Account', balance=100, account_type='CASH', budget=self.budget).exists())
      self.assertRedirects(response, reverse('financeapp:account_list'))
      
    #Test for Add Money to Account 
    def test_add_money_to_account_view(self):
      self.set_session()
      
      account = Account.objects.create(account_name='Test Account', account_type='CASH', balance=100, budget=self.budget)
      
      form_data = {
        'account_id': account.id,
        'amount': 100
      }
      
      response = self.client.post(reverse('financeapp:add_money_to_account'), form_data)
      self.assertEqual(response.status_code, 302)
      self.assertTrue(Account.objects.filter(account_name='Test Account', balance=200, account_type='CASH', budget=self.budget).exists())
      self.assertRedirects(response, reverse('financeapp:account_list'))
      
    #Test for Profile
    def test_user_profile_view(self):
      response = self.client.get(reverse('financeapp:profile'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'financeapp/profile.html')
      
    #Test for add_zero_based_category
    def test_add_zero_based_category_view(self):
      self.set_session()
      
      form_data = {
        'name': 'Test Category',
        'assigned_amount': 100,
      }
      
      response = self.client.post(reverse('financeapp:add_zero_category', args=[self.budget.id]), form_data)
      self.assertEqual(response.status_code, 302)
      self.assertTrue(ZeroBasedCategory.objects.filter(name='Test Category', assigned_amount=100, budget=self.budget).exists())
      self.assertRedirects(response, reverse('financeapp:zero_based_page', args=[self.budget.id]))
      
    #Test for edit_zero_based_category
    def test_edit_zero_based_category_view(self):
      self.set_session()
      
      category = ZeroBasedCategory.objects.create(name='Test Category', assigned_amount=100, budget=self.budget)
      
      form_data = {
        'category_id': category.id,
        'name': 'Test Category',
        'assigned_amount': 200
        
      }
      
      response = self.client.post(reverse('financeapp:edit_zero_category', args=[self.budget.id]), form_data)
      self.assertEqual(response.status_code, 302)
      self.assertTrue(ZeroBasedCategory.objects.filter(name='Test Category', assigned_amount=200, budget=self.budget).exists())
      self.assertRedirects(response, reverse('financeapp:zero_based_page', args=[self.budget.id]))
    
    #Test for delete_zero_category
    def test_delete_zero_category_view(self):
      self.set_session()
      
      category = ZeroBasedCategory.objects.create(name='Test Category', assigned_amount=100, budget=self.budget)
      
      response = self.client.post(reverse('financeapp:delete_zero_category', args=[self.budget.id]), {'category_id': category.id})
      self.assertEqual(response.status_code, 302)
      self.assertFalse(ZeroBasedCategory.objects.filter(name='Test Category', assigned_amount=100, budget=self.budget).exists())
      self.assertRedirects(response, reverse('financeapp:zero_based_page', args=[self.budget.id]))
    
    #Test for add_zero_expense
    def test_add_zero_based_expense_view(self):
      self.set_session()
      
      category = ZeroBasedCategory.objects.create(name='Test Category', assigned_amount=100, budget=self.budget)
      
      form_data = {
        'category_id': category.id,
        'description': 'Test Expense',
        'assigned_amount': 50,   
      }
      
      response = self.client.post(reverse('financeapp:add_zero_expense', args=[self.budget.id]), form_data)
      self.assertEqual(response.status_code, 302)
      self.assertTrue(Expense.objects.filter(category=category, description='Test Expense', assigned_amount=50).exists())
      
       #Test for add_zero_based_expense 
    def test_edit_zero_based_expense_view(self):
      self.set_session()
      category = ZeroBasedCategory.objects.create(name='Test Category', assigned_amount=100, budget=self.budget)
      expense = Expense.objects.create(category=category, description='Test Expense', assigned_amount=50)
        
      form_data = {
        'expense_id': expense.id,
        'category_id': category.id,
        'description': 'Test Expense',
        'assigned_amount': 200
         }
      response = self.client.post(reverse('financeapp:edit_zero_expense', args=[self.budget.id]), form_data)
      self.assertEqual(response.status_code, 302)
      self.assertTrue(Expense.objects.filter(category=category, description='Test Expense', assigned_amount=200).exists())
      self.assertRedirects(response, reverse('financeapp:zero_based_page', args=[self.budget.id]))
      
    #Test for delete_zero_expense
    def test_delete_zero_based_expense_view(self):
      self.set_session()
      
      category = ZeroBasedCategory.objects.create(name='Test Category', assigned_amount=100, budget=self.budget)
      expense = Expense.objects.create(category=category, description='Test Expense', assigned_amount=50)
      
      response = self.client.post(reverse('financeapp:delete_zero_expense', args=[self.budget.id]), {'expense_id': expense.id, 'category_id': category.id})
      self.assertEqual(response.status_code, 302)
      self.assertFalse(Expense.objects.filter(category=category, description='Test Expense', assigned_amount=50).exists())
      self.assertRedirects(response, reverse('financeapp:zero_based_page', args=[self.budget.id]))

      
    def test_recurring_category_and_expense_in_next_month(self):
      self.set_session()

    # Set up the initial category and expense
      initial_month = timezone.now().replace(day=1)  # Get the first day of the current month
      next_month = (initial_month + datetime.timedelta(days=31)).replace(day=1)  # Get the first day of the next month
    
      # Create a recurring category
      category = ZeroBasedCategory.objects.create(
          name='Recurring Category', 
          assigned_amount=100, 
          budget=self.budget, 
          month=initial_month, 
          is_recurring=True
      )
    
      # Create a recurring expense within the category
      expense = Expense.objects.create(
          category=category, 
          description='Recurring Expense', 
          assigned_amount=50, 
          spent=0, 
          is_recurring=True
    )
    
      # Simulate the user moving to the next month's budget
      response = self.client.get(reverse('financeapp:zero_based_page_with_date', args=[self.budget.id, next_month.year, next_month.month]))
      self.assertEqual(response.status_code, 200)
    
      # Check if the recurring category exists in the next month's budget
      next_month_category = ZeroBasedCategory.objects.filter(
        name='Recurring Category', 
        budget=self.budget, 
        month=next_month,
        is_recurring=True
    ).exists()
      self.assertTrue(next_month_category)
    
    # Check if the recurring expense exists in the next month's category
      next_month_expense = Expense.objects.filter(
          category__name='Recurring Category', 
          description='Recurring Expense', 
          assigned_amount=50, 
          category__budget=self.budget, 
          category__month=next_month,
          is_recurring=True
    ).exists()
      self.assertTrue(next_month_expense)
      
    def set_session_for_fifty(self):
      session = self.client.session
      session['selected_budget_id'] = self.fifty_thirty_twenty_budget.id
      session.save()
      
    #Test for 50.30.20 Budget
    
    def test_fifty_thirty_twenty_page_view(self):
      self.set_session_for_fifty()
      
      response = self.client.get(reverse('financeapp:fifty_thirty_twenty_page', args=[self.fifty_thirty_twenty_budget.id]))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'financeapp/fifty_thirty_twenty_budget_detail.html')
      
    #Test for add_fifty_thirty_twenty_expense
    def test_Needs_Wants_Savings_Category_were_created(self):
      self.set_session_for_fifty()
      
      # Ensure categories associated with the budget were created
      needs_category = FiftyThirtyTwentyCategory.objects.filter(
        budget=self.fifty_thirty_twenty_budget,
        name='Needs'
        ).exists()

      wants_category = FiftyThirtyTwentyCategory.objects.filter(
        budget=self.fifty_thirty_twenty_budget,
        name='Wants'
        ).exists()

      savings_category = FiftyThirtyTwentyCategory.objects.filter(
        budget=self.fifty_thirty_twenty_budget,
        name='Savings'
       ).exists()

      # Assertions to check that all categories were created
      self.assertTrue(needs_category, "Needs category was not created")
      self.assertTrue(wants_category, "Wants category was not created")
      self.assertTrue(savings_category, "Savings category was not created")
      
    def test_add_fifty_thirty_twenty_expense_view(self):
      self.set_session_for_fifty()
      
      #Get the Needs Category
      needs_category = FiftyThirtyTwentyCategory.objects.get(budget=self.fifty_thirty_twenty_budget, name='Needs')
      
      #give the need category an assigned amount
      needs_category.assigned_amount = 50
      needs_category.save()
    
      
      #Create a form data for the expense
      form_data = {
        'fifty_30_twenty_category_id': needs_category.id, 
        'description': 'Test Expense',
        'assigned_amount': 50
      }
      
      #Post the form data
      response = self.client.post(reverse('financeapp:add_fifty_thirty_twenty_expense', args=[self.fifty_thirty_twenty_budget.id]),  form_data)
      
      self.assertEqual(response.status_code, 302)
      self.assertTrue(Expense.objects.filter(fifty_30_twenty_category=needs_category, description='Test Expense', assigned_amount=50).exists())
      self.assertRedirects(response, reverse('financeapp:fifty_thirty_twenty_page', args=[self.fifty_thirty_twenty_budget.id]))
      
  
    def test_edit_fifty_thirty_twenty_expense_view(self):
      self.set_session_for_fifty()
      
      # Get the Needs Category
      wants_category = FiftyThirtyTwentyCategory.objects.get(budget=self.fifty_thirty_twenty_budget, name='Wants')
      
      # Create an expense within the Needs Category
      expense = Expense.objects.create(
        fifty_30_twenty_category=wants_category, 
        description='Test Expense', 
        assigned_amount=50
      )
      
      # Create a form data for the expense
      form_data = {
        'expense_id': expense.id,
        'fifty_30_twenty_category_id': wants_category.id, 
        'description': 'Test Expense',
        'assigned_amount': 100
      }
      
      # Post the form data
      response = self.client.post(reverse('financeapp:edit_fifty_thirty_twenty_expense', args=[self.fifty_thirty_twenty_budget.id]), form_data)
      
      self.assertEqual(response.status_code, 302)
      self.assertTrue(Expense.objects.filter(fifty_30_twenty_category=wants_category, description='Test Expense', assigned_amount=100).exists())
      self.assertRedirects(response, reverse('financeapp:fifty_thirty_twenty_page', args=[self.fifty_thirty_twenty_budget.id]))
      
      
    def test_delete_fifty_thirty_twenty_expense_view(self):
      self.set_session_for_fifty()
        
      # Get the Needs Category
      savings_category = FiftyThirtyTwentyCategory.objects.get(budget=self.fifty_thirty_twenty_budget, name='Savings')
        
      # Create an expense within the Needs Category
      expense = Expense.objects.create(
        fifty_30_twenty_category=savings_category, 
        description='Test Expense', 
        assigned_amount=50
      )
      
      form_data = {
        'expense_id': expense.id,
        'fifty_30_twenty_category_id': savings_category.id
      }
        
      # Post the form data
      response = self.client.post(reverse('financeapp:delete_expense', args=[self.fifty_thirty_twenty_budget.id]), form_data)
        
      self.assertEqual(response.status_code, 302)
      self.assertFalse(Expense.objects.filter(fifty_30_twenty_category=savings_category, description='Test Expense', assigned_amount=50).exists())
      self.assertRedirects(response, reverse('financeapp:fifty_thirty_twenty_page', args=[self.fifty_thirty_twenty_budget.id]))
    
    #Test for recurring category and expense in next month
    def test_recurring_fifty_thirty_twenty_category_and_expense_in_next_month(self):
      self.set_session_for_fifty()
      
      # Set up the initial category and expense
      initial_month = timezone.now().replace(day=1)  # Get the first day of the current month
      next_month = (initial_month + datetime.timedelta(days=31)).replace(day=1)  # Get the first day of the next month
      
      # Create a recurring category
      savings_category = FiftyThirtyTwentyCategory.objects.get(budget=self.fifty_thirty_twenty_budget, name='Savings')
      
      # Create a recurring expense within the category
      expense = Expense.objects.create(
          fifty_30_twenty_category=savings_category, 
          description='Recurring Expense', 
          assigned_amount=50, 
          spent=0, 
          is_recurring=True
      )
      
      # Simulate the user moving to the next month's budget
      response = self.client.get(reverse('financeapp:fifty_thirty_twenty_page_with_date', args=[self.fifty_thirty_twenty_budget.id, next_month.year, next_month.month]))
      self.assertEqual(response.status_code, 200)
      
      # Check if the recurring category exists in the next month's budget
      next_month_category = FiftyThirtyTwentyCategory.objects.filter(
          name='Savings', 
          budget=self.fifty_thirty_twenty_budget, 
          month=next_month,
          is_recurring=True
      ).exists()
      
      # Check if the recurring expense exists in the next month's category
      next_month_expense = Expense.objects.filter(
          fifty_30_twenty_category__name='Savings', 
          description='Recurring Expense', 
          assigned_amount=50, 
          fifty_30_twenty_category__budget=self.fifty_thirty_twenty_budget, 
          fifty_30_twenty_category__month=next_month,
          is_recurring=True
      ).exists()
      self.assertTrue(next_month_expense)
      
    #Test Transaction
    #Test inflow Transaction
    def test_add_transaction(self):
      self.set_session()
      account = Account.objects.create(account_name='Test_Account', account_type='CASH', balance=100, budget=self.budget)
       # Test that the initial transaction was created
      initial_transaction = Transaction.objects.filter(account=account, description__startswith='Initial balance').first()
      self.assertIsNotNone(initial_transaction, "Initial transaction was not created.")
      self.assertEqual(initial_transaction.inflow, 100)
      self.assertEqual(initial_transaction.outflow, 0)
      self.assertTrue(initial_transaction.created_by_account)
      # Create an inflow transaction
      inflow_amount = 50
      transaction_inflow = Transaction.objects.create(
          account=account,
          inflow=inflow_amount,
          outflow=0,
          description='Test Inflow',
          date=timezone.now()
        )
       # Assert the balance has been correctly updated
      self.assertEqual(account.balance, 150, "Account balance did not update correctly.")
      self.assertEqual(transaction_inflow.account, account)
      self.assertEqual(transaction_inflow.inflow, inflow_amount)
      
      self.assertEqual(transaction_inflow.outflow, 0)
      # Check that the transaction was created and linked to the account
      self.assertIsNotNone(transaction_inflow.id, "Inflow transaction was not created.")
      
      #Test outflow Transaction
      category = ZeroBasedCategory.objects.create(name='Test Category', assigned_amount=100, budget=self.budget)
      expense = Expense.objects.create(category=category, description='Test Expense', assigned_amount=50)
      
      outflow_amount = 50
      transaction_outflow = Transaction.objects.create(
        account=account,
        expense=expense,
        inflow=0,
        outflow=outflow_amount,
        description='Test Outflow',
        date=timezone.now()
       
      )
      self.assertEqual(account.balance, 100, "Account balance did not update correctly.")
      self.assertEqual(transaction_outflow.account, account)
      self.assertEqual(transaction_outflow.outflow, outflow_amount)
      self.assertEqual(expense.spent, 50)
      
      self.assertEqual(transaction_outflow.inflow, 0)
      self.assertIsNotNone(transaction_outflow.id, "outflow transaction was not created.")
      
      
    #Test edit Transaction
    def test_edit_transaction(self):
      self.set_session()
      category = ZeroBasedCategory.objects.create(name='Test Category', assigned_amount=100, budget=self.budget)
      account = Account.objects.create(account_name='Test_Account', account_type='CASH', balance=100, budget=self.budget)
      expense = Expense.objects.create(category=category, description='Test Expense', assigned_amount=50)
        
      outflow_amount = 40
      transaction = Transaction.objects.create(
        account=account,
        expense=expense,
        inflow=0,
        outflow=outflow_amount,
        description='Test Outflow',
        date=timezone.now().strftime('%Y-%m-%d'),
          )
      
      new_outflow_amount = 60
      form_data = {
        'transaction_id': transaction.id,
        'expense': expense.id,
        'account': account.id,    
        'description': 'Test Outflow',
        'outflow': new_outflow_amount,  # Change the outflow amount
        'date': timezone.now().strftime('%Y-%m-%d'),  # Ensure the date is in the correct format
        'inflow': 0,  # Include inflow as it's a required field
        }

      
      response = self.client.post(reverse('financeapp:edit_transaction'), form_data)

      self.assertEqual(response.status_code, 302)
      self.assertTrue(Transaction.objects.filter(expense=expense, account=account, description='Test Outflow', outflow=new_outflow_amount).exists())
      account.refresh_from_db()
      self.assertEqual(account.balance, 40)  # 100 - 60 = 40
      expense.refresh_from_db()
      self.assertEqual(expense.spent, 60)
        
    #Test delete Transaction
    def test_delete_transaction(self):
      self.set_session()
      category = ZeroBasedCategory.objects.create(name='Test Category', assigned_amount=100, budget=self.budget)
      account = Account.objects.create(account_name='Test_Account', account_type='CASH', balance=100, budget=self.budget)
      expense = Expense.objects.create(category=category, description='Test Expense', assigned_amount=50)
        
        
      outflow_amount = 40
      transaction_outflow = Transaction.objects.create(
        account=account,
        expense=expense,
        inflow=0,
        outflow=outflow_amount,
        description='Test Outflow',
        date=timezone.now()  
        )
      # Assert initial conditions
      self.assertEqual(account.balance, 60, "Initial balance did not update correctly after transaction.")  # 100 - 40 = 60
      
      form_data = {
        'transaction_id': transaction_outflow.id,
       
        }
      
        
      response = self.client.post(reverse('financeapp:delete_transaction'), form_data)
      if response.context and 'form' in response.context:
        print("Form errors:", response.context['form'].errors)  # Print form errors for debugging

      self.assertEqual(response.status_code, 302)
      # Ensure the transaction has been deleted
      transaction_exists = Transaction.objects.filter(id=transaction_outflow.id).exists()
      self.assertFalse(transaction_exists, "Transaction was not deleted.")

      self.assertFalse(Transaction.objects.filter(id=transaction_outflow.id).exists(), "Transaction was not deleted.")  
      account.refresh_from_db()
      self.assertEqual(account.balance, 100)
     
