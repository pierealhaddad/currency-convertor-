import tkinter as tk
from tkinter import ttk, messagebox
import requests

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x300")
        
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.exchange_rates = self.get_exchange_rates()
        
        ttk.Label(root, text="Amount:").pack(pady=5)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.pack(pady=5)
        
        ttk.Label(root, text="From Currency:").pack(pady=5)
        self.from_currency = ttk.Combobox(root, values=list(self.exchange_rates.keys()))
        self.from_currency.pack(pady=5)
        self.from_currency.set("USD")
        
        ttk.Label(root, text="To Currency:").pack(pady=5)
        self.to_currency = ttk.Combobox(root, values=list(self.exchange_rates.keys()))
        self.to_currency.pack(pady=5)
        self.to_currency.set("EUR")
        
        self.convert_button = ttk.Button(root, text="Convert", command=self.convert_currency)
        self.convert_button.pack(pady=10)
        
        self.result_label = ttk.Label(root, text="Converted Amount: ")
        self.result_label.pack(pady=5)
    
    def get_exchange_rates(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            return data["rates"]
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch exchange rates: {e}")
            return {}
    
    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency.get()
            to_currency = self.to_currency.get()
            
            if from_currency not in self.exchange_rates or to_currency not in self.exchange_rates:
                messagebox.showerror("Error", "Invalid currency selection.")
                return
            
            converted_amount = amount * (self.exchange_rates[to_currency] / self.exchange_rates[from_currency])
            self.result_label.config(text=f"Converted Amount: {converted_amount:.2f} {to_currency}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the amount.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()