from accounts import Account
import gradio as gr

# Initialize the account with a starting balance
account = Account(initial_balance=100.0)

def deposit(amount: float):
    try:
        account.deposit(amount)
        return f"Deposited ${amount}. New balance: ${account.get_balance()}"
    except ValueError as e:
        return str(e)

def withdraw(amount: float):
    if account.withdraw(amount):
        return f"Withdrew ${amount}. New balance: ${account.get_balance()}"
    else:
        return "Withdrawal failed: insufficient funds."

def check_balance():
    return f"Current balance: ${account.get_balance()}"

# Create Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## Simple Account Management")
    
    with gr.Row():
        deposit_amount = gr.Number(label="Deposit Amount", value=0)
        deposit_button = gr.Button("Deposit")
        
    deposit_output = gr.Textbox(label="Deposit Result")

    with gr.Row():
        withdraw_amount = gr.Number(label="Withdraw Amount", value=0)
        withdraw_button = gr.Button("Withdraw")
    
    withdraw_output = gr.Textbox(label="Withdraw Result")

    balance_button = gr.Button("Check Balance")
    balance_output = gr.Textbox(label="Balance")

    deposit_button.click(fn=deposit, inputs=deposit_amount, outputs=deposit_output)
    withdraw_button.click(fn=withdraw, inputs=withdraw_amount, outputs=withdraw_output)
    balance_button.click(fn=check_balance, outputs=balance_output)

demo.launch()