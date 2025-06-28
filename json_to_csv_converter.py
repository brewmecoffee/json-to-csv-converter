import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import json
import csv
import threading
from pathlib import Path
import os


class JSONToCSVConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON to CSV Converter")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.selected_files = []
        self.output_folder = ""
        
        # Style configuration
        self.setup_styles()
        
        # Create GUI elements
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Action.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=(10, 5))
        
        # Configure label styles
        style.configure('Title.TLabel',
                       font=('Arial', 16, 'bold'),
                       foreground='#2c3e50')
        
        style.configure('Header.TLabel',
                       font=('Arial', 12, 'bold'),
                       foreground='#34495e')
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="JSON to CSV Converter", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        ttk.Label(main_frame, text="Select JSON Files:", style='Header.TLabel').grid(
            row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        # File selection frame
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        
        # Listbox for selected files
        self.file_listbox = tk.Listbox(file_frame, height=8, selectmode=tk.EXTENDED,
                                      bg="white", font=('Arial', 9))
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Buttons
        ttk.Button(button_frame, text="Add JSON Files", command=self.add_files, 
                  style='Action.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_files,
                  style='Action.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_files,
                  style='Action.TButton').grid(row=0, column=2, padx=5)
        
        # Output folder section
        ttk.Label(main_frame, text="Output Folder:", style='Header.TLabel').grid(
            row=4, column=0, sticky=tk.W, pady=(20, 5))
        
        # Output folder frame
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var, 
                                     font=('Arial', 9), state='readonly')
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(output_frame, text="Browse", command=self.select_output_folder).grid(
            row=0, column=1)
        
        # Progress section
        ttk.Label(main_frame, text="Progress:", style='Header.TLabel').grid(
            row=6, column=0, sticky=tk.W, pady=(20, 5))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to convert files...")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=('Arial', 9), foreground='#7f8c8d')
        status_label.grid(row=8, column=0, columnspan=3, pady=(0, 20))
        
        # Convert button
        self.convert_button = ttk.Button(main_frame, text="Convert to CSV", 
                                        command=self.start_conversion, 
                                        style='Action.TButton')
        self.convert_button.grid(row=9, column=0, columnspan=3, pady=10)
        
        # Results section
        ttk.Label(main_frame, text="Conversion Results:", style='Header.TLabel').grid(
            row=10, column=0, sticky=tk.W, pady=(20, 5))
        
        # Results text area
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=11, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(11, weight=1)
        
        self.results_text = tk.Text(results_frame, height=6, wrap=tk.WORD, 
                                   bg="white", font=('Arial', 9))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Scrollbar for results
        results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, 
                                         command=self.results_text.yview)
        results_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select JSON Files",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
        
        # Limit to 50 files
        if len(self.selected_files) > 50:
            messagebox.showwarning("File Limit", 
                                 "Maximum 50 files allowed. Only the first 50 files will be kept.")
            self.selected_files = self.selected_files[:50]
        
        self.update_file_list()
        
    def remove_files(self):
        selected_indices = self.file_listbox.curselection()
        for index in reversed(selected_indices):
            del self.selected_files[index]
        self.update_file_list()
        
    def clear_files(self):
        self.selected_files.clear()
        self.update_file_list()
        
    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for file in self.selected_files:
            filename = Path(file).name
            self.file_listbox.insert(tk.END, filename)
        
        # Update status
        count = len(self.selected_files)
        if count == 0:
            self.status_var.set("No files selected...")
        else:
            self.status_var.set(f"{count} file(s) selected (Max: 50)")
        
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_var.set(folder)
            
    def start_conversion(self):
        if not self.selected_files:
            messagebox.showerror("Error", "Please select at least one JSON file.")
            return
            
        if not self.output_folder:
            messagebox.showerror("Error", "Please select an output folder.")
            return
        
        # Disable convert button during conversion
        self.convert_button.configure(state='disabled')
        self.results_text.delete(1.0, tk.END)
        
        # Start conversion in a separate thread
        thread = threading.Thread(target=self.convert_files)
        thread.daemon = True
        thread.start()
        
    def convert_files(self):
        successful_conversions = 0
        failed_conversions = 0
        
        total_files = len(self.selected_files)
        
        for i, json_file in enumerate(self.selected_files):
            try:
                # Update progress
                progress = (i / total_files) * 100
                self.progress_var.set(progress)
                self.status_var.set(f"Converting {Path(json_file).name}...")
                
                # Read JSON file
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert to DataFrame
                if isinstance(data, list):
                    df = pd.json_normalize(data)
                elif isinstance(data, dict):
                    df = pd.json_normalize([data])
                else:
                    raise ValueError("JSON must contain a list or dictionary")
                
                # Generate output filename
                input_filename = Path(json_file).stem
                output_file = os.path.join(self.output_folder, f"{input_filename}.csv")
                
                # Save as CSV
                df.to_csv(output_file, index=False, encoding='utf-8')
                
                # Update results
                self.results_text.insert(tk.END, f"✓ {Path(json_file).name} → {Path(output_file).name}\n")
                successful_conversions += 1
                
            except Exception as e:
                # Update results with error
                self.results_text.insert(tk.END, f"✗ {Path(json_file).name} - Error: {str(e)}\n")
                failed_conversions += 1
                
            # Scroll to bottom
            self.results_text.see(tk.END)
            self.root.update()
        
        # Finalize
        self.progress_var.set(100)
        self.status_var.set(f"Conversion complete! {successful_conversions} successful, {failed_conversions} failed")
        
        # Re-enable convert button
        self.convert_button.configure(state='normal')
        
        # Show completion message
        if failed_conversions == 0:
            messagebox.showinfo("Success", f"All {successful_conversions} files converted successfully!")
        else:
            messagebox.showwarning("Partial Success", 
                                 f"{successful_conversions} files converted successfully, "
                                 f"{failed_conversions} files failed.")


def main():
    root = tk.Tk()
    app = JSONToCSVConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
