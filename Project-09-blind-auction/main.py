import tkinter as tk
from tkinter import messagebox

class AuctionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blind Auction")
        self.geometry("400x400")
        self.bids = {}

        # Title
        self.title_label = tk.Label(self, text="🏆 Blind Auction 🏆", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=10)

        # Name input
        self.name_label = tk.Label(self, text="Enter your name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.pack(pady=5)

        # Bid input
        self.bid_label = tk.Label(self, text="Enter your bid ($):")
        self.bid_label.pack()
        self.bid_entry = tk.Entry(self, width=30)
        self.bid_entry.pack(pady=5)

        # Buttons
        self.add_button = tk.Button(self, text="Add Bidder", command=self.add_bidder)
        self.add_button.pack(pady=5)

        self.finish_button = tk.Button(self, text="Finish Auction", command=self.finish_auction)
        self.finish_button.pack(pady=5)

        # Listbox to show bidders
        self.listbox_label = tk.Label(self, text="Bidders so far:")
        self.listbox_label.pack()
        self.listbox = tk.Listbox(self, width=40, height=8)
        self.listbox.pack(pady=5)

    def add_bidder(self):
        name = self.name_entry.get().strip()
        bid = self.bid_entry.get().strip()

        if not name or not bid:
            messagebox.showerror("Error", "Please enter both name and bid!")
            return
        if not bid.isdigit():
            messagebox.showerror("Error", "Bid must be a number!")
            return

        bid = int(bid)
        self.bids[name] = bid
        self.listbox.insert(tk.END, f"{name} - ${bid}")

        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.bid_entry.delete(0, tk.END)

    def finish_auction(self):
        if not self.bids:
            messagebox.showwarning("Warning", "No bids placed yet!")
            return

        highest_bid = max(self.bids.values())
        winners = [name for name, bid in self.bids.items() if bid == highest_bid]

        if len(winners) == 1:
            messagebox.showinfo("Winner", f"🏆 The winner is {winners[0]} with a bid of ${highest_bid}!")
        else:
            tied = ", ".join(winners)
            messagebox.showinfo("Tie", f"🤝 It's a tie between {tied} with a bid of ${highest_bid}!")

        # Reset auction
        self.bids.clear()
        self.listbox.delete(0, tk.END)

if __name__ == "__main__":
    app = AuctionApp()
    app.mainloop()
