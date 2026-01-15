# Gmail to Google Sheets Automation

**Author:** Akshat Jain

## 📖 Project Overview
This project is a Python automation system that reads real unread emails
from a Gmail account and logs them into a Google Sheet using Google APIs.

---

## 🏗️ Architecture
Gmail (Unread Emails)
        ↓
        
Gmail API (OAuth 2.0)
        ↓
        
Python Automation Script
        ↓
        
Google Sheets API

---

## ⚙️ Technologies Used
- Python 3
- Gmail API
- Google Sheets API
- OAuth 2.0
- Google Cloud Platform

---

## 🔐 OAuth Flow Explanation
The project uses OAuth 2.0 Desktop flow. On the first run, the user is
redirected to Google's consent screen to grant access to Gmail and Google
Sheets. The generated token is stored locally and reused for subsequent
runs, avoiding repeated authentication.

---

## 🔁 Duplicate Prevention & State Management
Each Gmail message has a unique message ID.  
Processed message IDs are stored in a local file (`processed_ids.txt`).

On every execution:
- New unread emails are fetched
- Message IDs are checked against stored IDs
- Already processed emails are skipped

This ensures idempotent execution and prevents duplicate rows in Google Sheets.

---
