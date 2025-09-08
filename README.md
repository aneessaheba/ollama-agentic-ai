
# Homework 1 - Distributed Systems for Data Engineering  
**Course:** DATA-236  
**Name:** Anees Saheba Guddi  
**Student ID:** 018205330  
**Date:** Sept 8, 2025  

---

## 📌 Part 1: HTML + JavaScript

### ✅ HTML
- Created a page with title `HW1-AneesSahebaGuddi`.
- Added a heading for **Blog Topic**.
- Built a form containing:
  - Blog Title (required, autofocus)  
  - Author Name (required)  
  - Email (required)  
  - Blog Content (required)  
  - Dropdown (Technology, Lifestyle, Travel, Education)  
  - Terms & Conditions checkbox (required)  
  - **Publish Blog** button  

**Screenshot (Form Page):**  
![Form Page](page_1_img_1.png)

### ✅ JavaScript Features
- Validation for blog content (must be > 25 characters).  
- Validation for Terms & Conditions checkbox.  
- Converted form data to **JSON** and logged it.  
- Used **object destructuring** (extract `title` and `email`).  
- Added `submissionDate` using **spread operator**.  
- Implemented **closure** to count successful submissions.  

**Code Screenshot:**  
![HTML Code](page_2_img_2.png)  
![JavaScript Code](page_2_img_3.png)  

**Validation Example:**  
![Validation Blog Content](page_3_img_4.png)  
![Validation Checkbox](page_3_img_5.png)  

---

## 📌 Part 2: Deployment

### 🚀 Docker
- Built Docker image for the application.  
- Ran container locally (app accessible on `localhost:8080`).  

**Docker Screenshots:**  
![Docker Images](page_4_img_6.png)  
![Docker Containers](page_4_img_7.png)  

### ☁️ AWS ECS
- Deployed containerized app to AWS ECS.  
- App running on **Public IP Address**.  

**Screenshots:**  
![Localhost Running](page_5_img_8.png)  
![AWS ECS Running](page_5_img_9.png)  

---

## 📌 Part 3: Agentic AI with Ollama

### ✅ Setup
- Installed and ran **Ollama** with model `smollm:1.7b` and `Phi3:mini`.  

**Screenshot:**  
![Ollama Setup](page_6_img_10.png)  

### ✅ Python Script
- Wrote `agents_demo.py` to demonstrate multi-agent workflow.  

**Screenshot:**  
![Python Script](page_6_img_11.png)  

### ✅ Deliverables
- Output includes **Planner**, **Reviewer**, and **Finalizer** stages.  
- Published package contains:
  - Blog Title & Content  
  - Tags  
  - Summary  
  - Reviews & Issues  
  - Submission Date  

**Output Screenshot:**  
![Deliverables](page_7_img_12.png)  

---

## 📌 Q&A

**Q1. Final Tags**  
- Planner: `["malware", "phishing", "ransomware"]`  
- Reviewer: `["malware", "phishing", "ransomware"]`  
- Final: `["introduction", "to", "cybersecurity"]`  

**Q2. Final Summary (≤25 words)**  
> "Brief overview of Introduction to Cybersecurity Threats."  

**Q3. Reviewer Changes**  
- Reviewer did not change tags but expanded the summary with detailed recommendations.  

**Q4. Step Explanation**  
- **Planner**: Generates initial tags and summary.  
- **Reviewer**: Validates and improves Planner output.  
- **Finalizer**: Consolidates outputs and prepares publishable package.  

---

## 🛠️ Tech Stack
- **HTML5, CSS, JavaScript**  
- **Docker, AWS ECS**  
- **Ollama (smollm:1.7b, Phi3:mini)**  
- **Python (agents_demo.py)**  

