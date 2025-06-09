# **Quiz-Application: Java & Python ML Integration**

### **Overview**
🚀 Welcome to the **Quiz-Application**, a Java-based interactive quiz system enhanced with **Python ML integration**! This project allows users to upload a **PDF document**, which is processed using **machine learning** in Python to extract key information and generate **dynamic quiz questions**. The quiz is then conducted within a sleek **Java Swing UI**, making it a powerful educational tool.

### **Features**
🔹 **Drag & Drop PDF Upload** – Users can drop a PDF file into the Java application, which is then sent to a Python service for processing.  
🔹 **ML-Based Question Generation** – The Python backend extracts key details from the document and dynamically creates quiz questions using an **AI-powered language model**.  
🔹 **Responsive & Interactive UI** – A well-designed **Java Swing** interface allows users to take the quiz with a **timer-based question flow**.  
🔹 **Automatic Score Calculation** – The application evaluates user responses and displays results instantly.  
🔹 **Seamless Java-Python Communication** – REST API integration enables smooth data exchange between the **Java quiz interface** and the **Python ML backend**.

### **Technology Stack**
✅ **Java Swing** – UI for user interaction  
✅ **Python (Flask, Ollama, pdf2image)** – ML-powered document processing  
✅ **Jackson (JSON Parsing)** – Converts Python ML output to structured quiz questions in Java  
✅ **REST API** – Java sends files to Python & retrieves generated questions  
✅ **Multithreading & Timer** – Time-limited quiz functionality  

### **How It Works**
1️⃣ **User Uploads PDF** → Java sends the file to Python via REST API.  
2️⃣ **ML Model Processes PDF** → Python converts it to images, extracts textual info, and generates quiz questions.  
3️⃣ **Quiz Questions Sent Back to Java** → Java dynamically loads the quiz with AI-generated questions.  
4️⃣ **User Takes the Quiz** → Timer-based quiz experience in Java Swing.  
5️⃣ **Score Displayed** → Java evaluates answers and provides instant feedback.

### **Installation & Setup**
1. **Clone the repository**  
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/Quiz-Application.git
   cd Quiz-Application
   ```
2. **Set up Python dependencies**  
   ```bash
   pip install flask ollama pdf2image
   ```
3. **Run the Python server**  
   ```bash
   python RAG_test.ipynb
   ```
4. **Open the Java project in VS Code and run Login.java**  
   - Ensure **Jackson JARs** are referenced (`lib/**/*.jar`).  
   - Press **F5** to run the Java application.  

### **Contributing**
We welcome contributors! Feel free to **submit pull requests**, raise **issues**, and help improve this AI-powered quiz experience. 🌟

---
