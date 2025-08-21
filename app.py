import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import logging

# Configure logging
logging.basicConfig(
    filename="scanner.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def scan_port(host, port, results_box):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        if result == 0:
            msg = f"Port {port}: OPEN"
            results_box.insert(tk.END, msg)
            logging.info(msg)
        sock.close()
    except Exception as e:
        logging.error(f"Error scanning port {port}: {e}")

def start_scan(host_entry, start_entry, end_entry, results_box):
    host = host_entry.get().strip()
    try:
        start_port = int(start_entry.get())
        end_port = int(end_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Ports must be integers")
        return

    results_box.delete(0, tk.END)
    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(host, port, results_box))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def main():
    root = tk.Tk()
    root.title("Multi-threaded Port Scanner")

    tk.Label(root, text="Host:").grid(row=0, column=0, padx=5, pady=5)
    host_entry = tk.Entry(root, width=30)
    host_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Start Port:").grid(row=1, column=0, padx=5, pady=5)
    start_entry = tk.Entry(root, width=10)
    start_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    tk.Label(root, text="End Port:").grid(row=2, column=0, padx=5, pady=5)
    end_entry = tk.Entry(root, width=10)
    end_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    scan_btn = tk.Button(
        root, text="Start Scan",
        command=lambda: start_scan(host_entry, start_entry, end_entry, results_box)
    )
    scan_btn.grid(row=3, column=0, columnspan=2, pady=10)

    results_box = tk.Listbox(root, width=50, height=15)
    results_box.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
