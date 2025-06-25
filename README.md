# 🏥 Hospital Management - Odoo Module

## 📘 Overview

The **Hospital Management** module for Odoo helps healthcare institutions manage key operations across various departments. It integrates seamlessly with Odoo's backend to provide an efficient, user-friendly interface for staff to manage appointments, patient records, nursing tasks, newborns, pediatric care, and lab work.

---

## 🚀 Features

- 👤 **Patient Management**: Register and manage patient information.
- 📅 **Appointment Scheduling**: Track and manage doctor appointments.
- 🧑‍⚕️ **Nursing Dashboard**: Assign nurses and log medical care.
- 👶 **Newborn Records**: Maintain dedicated newborn profiles and logs.
- 👩‍👧 **Pediatric Care**: Specialized section for pediatric case handling.
- 🔬 **Laboratory Tracking**: Monitor lab tests and results.
- 📊 **Reports & Views**: Form, Tree, and Kanban views for efficient data handling.
- 🔐 **Role-based Access Control** (Optional depending on your module structure).

---

## 🛠️ Installation

### Prerequisites
- Odoo 18
- Python 3.x
- PostgreSQL

### Steps
1. Download or clone this repository:
    ```bash
    git clone https://your-repo-url.git
    ```
2. Copy the `Hospital_Management` folder to your Odoo `addons` directory:
    ```bash
    cp -r Hospital_Management /path/to/odoo/addons/
    ```
3. Restart the Odoo server:
    ```bash
    ./odoo-bin -u all -d your-database-name
    ```
4. Log in to Odoo, activate **Developer Mode**, then go to **Apps** > **Update Apps List**.
5. Search for "Hospital Management" and click **Install**.

---


## 🧭 Usage

After installation, navigate to the **Hospital** menu in the Odoo backend. Here you can:

- **Register patients**
- **Create and manage appointments**
- **Assign nurses and track their shifts**
- **Enter newborn records and pediatric assessments**
- **Schedule and view lab reports**

Each section offers intuitive forms and lists to help streamline operations.

---


