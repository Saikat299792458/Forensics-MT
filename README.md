# Forensics Model Test Generator (GUI)

A user-friendly **Model Test Generator** that allows you to create randomized model tests from text files and export them as **PDFs**.

This GUI-based tool enables easy file selection, customization of test parameters, and automatic PDF generation.

---

## 📌 Features

✅ **Select multiple text files** as input  
✅ **Remove unwanted files** before generating the test  
✅ **Set the number of model tests** to generate  
✅ **Choose an output location** for the PDF file  
✅ **Progress bar in a dialog box** for real-time updates  
✅ **Automatically opens the generated PDF** after creation  
✅ **Help link for user assistance**  

---

## 🛠️ Installation

### **Prerequisites**
- **Windows/macOS/Linux**  
- **Python 3.x** installed  
- Required libraries: `tkinter`, `reportlab`, `requests`

### **Setup Steps**
1. **Clone or Download the Repository**
   ```sh
   git clone https://github.com/yourrepo/model-test-generator.git
   cd model-test-generator
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```sh
   python app.py
   ```

---

## 🎮 Usage Guide

### **1️⃣ Add Input Files**
- Click **"Add input(\*.txt)"** to select multiple text files.
- The selected files appear in a **listbox**.
- Click **"Remove Selected"** to remove any unwanted files.

### **2️⃣ Choose Output PDF File**
- Click **"Choose Output(\*.pdf)"** to set the destination.
- The filename appears in a textbox.

### **3️⃣ Set Number of Tests**
- Enter the number of model tests in the **textbox**.

### **4️⃣ Generate the PDF**
- Click **"Generate PDF"** to start the process.
- A **progress dialog** appears, showing real-time progress.
- Once completed, the **PDF file opens automatically**.

---

## 🖼️ Screenshots

| Feature | Screenshot |
|---------|------------|
| **Main Interface** | ![GUI](screenshots/main.png) |
| **File Selection** | ![File Selection](screenshots/files.png) |
| **Progress Bar Dialog** | ![Progress](screenshots/progress.png) |

---

## ❓ FAQs

### **1. What file format should the input be in?**
- The tool accepts **plain text files (\*.txt)** where questions are categorized into:
  - **RECALL**
  - **Analytical**
  - **Problem Based**
- Analytical and Recall questions should be placed in single lines only. Problem based questions can have multi lines, but the start of a question must be marked by a * sign. You must add the title first "RECALL", or "ANALYTICAL", or "PROBLEM BASED" then add the related questions. Write the title correctly and do not add anything else in the title line, or the following questions may not be counted properly. For sample item questions please browse the repository.

### **2. Can I edit the PDF after generation?**
- No, but you can modify the text files before generating the PDF.

### **3. How can I update the tool?**
- Click on the **"Check for Updates"** link in the bottom right corner.

### **4. Where can I get help?**
- Click on the **"Help"** link in the bottom-right corner, which redirects to the official documentation page.

---

## 📝 License
This project is licensed under the **MIT License**.

---

## 🤝 Contributing
Contributions are welcome!  
Feel free to open an issue or submit a pull request. 🎯

