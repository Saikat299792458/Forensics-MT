import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import webbrowser
import importlib.util

pdfgen_path = os.path.join(os.getcwd(), "pdfgen.py")

def load_pdfgen():
    """Dynamically loads the pdfgen module from an external location."""
    if os.path.exists(pdfgen_path):
        spec = importlib.util.spec_from_file_location("pdfgen", pdfgen_path)
        pdfgen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pdfgen)
        return pdfgen
    else:
        raise ImportError("pdfgen.py not found!")

pdfgen = load_pdfgen()

def update():
    import requests
    url = "https://rentry.com/mdupdate"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file = open(pdfgen_path, "r")
            if response.content != file.read():
                file.close()
                file = open(pdfgen_path, "wb")
                file.write(response.content)
                messagebox.showinfo("Update", "Updated to latest version!")
                os.startfile()
            else:
                messagebox.showerror("Update", "No updates available!")
            file.close()
        else:
            raise Exception(response.status_code)
    except Exception as e:
        messagebox.showerror("Update Error", f"An Error Occured! Check your connection and try again. Error Code: {e}")


class ModelTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Model Test Generator")
        self.root.geometry("400x300")

        self.gen = pdfgen.pdfgen()  # Initialize the PDF generator logic

        self.create_widgets()

    def create_widgets(self):
        """Creates the UI elements for the application."""

        # File Selection Frame
        frame_files = tk.Frame(self.root)
        frame_files.pack(pady=5)

        # Listbox to display selected files
        self.listbox_files = tk.Listbox(frame_files, height=6, width=50, selectmode=tk.MULTIPLE)
        self.listbox_files.pack(side=tk.LEFT)

        # Scrollbar for Listbox
        scrollbar = tk.Scrollbar(frame_files, orient="vertical", command=self.listbox_files.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.listbox_files.config(yscrollcommand=scrollbar.set)

        # Frame for Add/Remove Buttons (Side by Side)
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        self.btn_choose_files = tk.Button(frame_buttons, text="Add input(*.txt)", command=self.choose_files)
        self.btn_choose_files.pack(side=tk.LEFT, padx=5)

        self.btn_remove_files = tk.Button(frame_buttons, text="Remove Selected", command=self.remove_selected_files)
        self.btn_remove_files.pack(side=tk.LEFT)

        # Frame for Output File Selection (Choose File Button + Textbox Side by Side)
        frame_output = tk.Frame(self.root)
        frame_output.pack(pady=15)

        self.btn_choose_output = tk.Button(frame_output, text="Choose Output(*.pdf)", command=self.choose_output)
        self.btn_choose_output.pack(side=tk.LEFT)

        self.entry_output = tk.Entry(frame_output, state='readonly', readonlybackground="white", font=("TkDefaultFont", 10))
        self.entry_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=3)  # Adjust ipady for height


        # Number of Model Tests Input
        frame_nbmt = tk.Frame(self.root)
        frame_nbmt.pack()
        self.lbl_tests = tk.Label(frame_nbmt, text="Number of Model Tests:")
        self.lbl_tests.pack(side=tk.LEFT)

        self.entry_tests = tk.Entry(frame_nbmt)
        self.entry_tests.pack(side=tk.LEFT)

        # Generate Button
        self.btn_generate = tk.Button(self.root, text="Generate PDF", command=self.generate_pdf)
        self.btn_generate.pack(pady=10)

        frame_help = tk.Frame(self.root)
        frame_help.pack(side=tk.TOP, anchor="ne", padx=10, pady=5)

        self.btn_help = tk.Label(frame_help, text="Help", fg="blue", cursor="hand2", font=("TkDefaultFont", 10, "underline"))
        self.btn_help.pack(side=tk.LEFT)
        self.btn_help.bind("<Button-1>", lambda e: webbrowser.open("https://google.com"))
        self.btn_update = tk.Label(frame_help, text="Check for Updates", fg="blue", cursor="hand2", font=("TkDefaultFont", 10, "underline"))
        self.btn_update.pack()
        self.btn_update.bind("<Button-1>", lambda e: update())


    def choose_files(self):
        """Opens file dialog to select multiple input text files and adds them to the listbox."""
        files = filedialog.askopenfilenames(title="Select Input Text Files", filetypes=[("Text Files", "*.txt")])
        if files:
            for file in files:
                if file not in self.gen.input_files:  # Prevent duplicates
                    self.gen.input_files.append(file)
                    self.listbox_files.insert(tk.END, os.path.basename(file))  # Show only filename

    def remove_selected_files(self):
        """Removes selected files from the listbox and internal list."""
        selected_indices = list(self.listbox_files.curselection())[::-1]  # Reverse order to avoid index shift issues
        for index in selected_indices:
            del self.gen.input_files[index]  # Remove from internal list
            self.listbox_files.delete(index)  # Remove from listbox

    def choose_output(self):
        """Opens save file dialog to choose output PDF filename and updates the textbox."""
        output_file = filedialog.asksaveasfilename(title="Save PDF As", defaultextension=".pdf",
                                                filetypes=[("PDF Files", "*.pdf")])
        if output_file:
            self.gen.output_filename = output_file
            self.entry_output.config(state='normal')  # Enable editing to update the text
            self.entry_output.delete(0, tk.END)  # Clear previous text
            self.entry_output.insert(0, os.path.basename(output_file))  # Show only filename
            self.entry_output.config(state='readonly')  # Make it readonly again


    def generate_pdf(self):
        """Generates the PDF file using selected input files and user-defined settings with a progress bar dialog."""
        
        # Validate Inputs
        if not self.gen.input_files:
            messagebox.showerror("Error", "Please select input text files.")
            return
        if not self.gen.output_filename:
            messagebox.showerror("Error", "Please choose an output file.")
            return
        try:
            num_tests = int(self.entry_tests.get())
            if num_tests < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of model tests.")
            return

        # Create Progress Dialog
        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title("Generating PDF")
        progress_dialog.geometry("300x100")
        progress_dialog.resizable(False, False)

        lbl_progress = tk.Label(progress_dialog, text="Generating, please wait...")
        lbl_progress.pack(pady=5)

        progress_bar = ttk.Progressbar(progress_dialog, orient="horizontal", length=250, mode="determinate")
        progress_bar.pack(pady=10)
        
        self.root.update_idletasks()  # Refresh UI

        # Read Questions from Input Files
        questions = self.gen.read_questions()

        if not questions:
            messagebox.showerror("Error", "No valid questions found in the input files.")
            progress_dialog.destroy()
            return

        # Generate PDF with progress updates
        for i in self.gen.create_pdf(num_tests, questions):
            progress_bar["value"] += i
            progress_dialog.update_idletasks()

        progress_dialog.destroy()  # Close the progress dialog when done

        # Show success message and open the PDF
        messagebox.showinfo("Success", "PDF generated successfully!")
        os.startfile(self.gen.output_filename)  # Open the generated PDF



# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ModelTestApp(root)
    root.mainloop()
