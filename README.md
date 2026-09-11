# 🛡️ AppSec Lab | Vulnerable & Hardened Web Infrastructure

<p align="left">
  <img src="https://img.shields.io/badge/UBUNTU-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu" />
  <img src="https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx" />
  <img src="https://img.shields.io/badge/PYTHON-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FLASK-3.0-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/SQLITE-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/OWASP-TOP_10-4B0082?style=for-the-badge" alt="OWASP" />
</p>

A full-stack, bare-metal-equivalent web application security research lab engineered on a virtualized **Ubuntu Linux** environment. This project demonstrates the lifecycle of modern web infrastructure: reverse proxy routing, asynchronous API bridging, and realistic **OWASP Top 10** vulnerability exploitation followed by defense-in-depth code remediation and kernel-level process isolation.

> [!NOTE]
> This laboratory is built for academic research and vulnerability demonstration. Ensure all testing is conducted inside isolated sandbox network adapters (Host-Only / NAT) to avoid accidental network exposure.

---

## 🛠️ Tech Stack and Architecture

* **Environment / Virtualization:** Ubuntu Linux (Guest OS) on Oracle VirtualBox
* **Reverse Proxy / Web Server:** Nginx (port 80)
* **Backend:** Python 3 + Flask (port 5000)
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3 (Modern Dark Theme), Vanilla JavaScript (Fetch API)

[Browser / Client]
│ (HTTP :80)
▼
[Nginx Reverse Proxy]
├── / ──> Serving static files (HTML/CSS/JS)
└── /api/* ──> Internal routing to Flask (:5000)
│
[Flask Backend]
│ (SQL Queries / Subprocess)
▼
[SQLite3 / Linux OS]

---

## 🎯 Completed Project Tasks (Stages 1–9)

1. **VM & Web Server:** Configuring the Nginx web server on an Ubuntu virtual machine.
2. **HTML:** Developing a semantic user interface structure.
3. **CSS:** Styling cards, forms, and layout using a modern dark theme.
4. **JavaScript:** Asynchronous DOM manipulation without page reloads.
5. **Web Application:** Building a server-side Flask application with routing support.
6. **Database Connection:** Integrating the SQLite relational database and initializing the data schema.
7. **REST APIs:** Exposing CRUD endpoints (`/api/posts`, `/api/search`, `/api/ping`).
8. **Vulnerability Testing:** Conducting controlled security exploits.
9. **Hardening & Remediation:** Patching vulnerabilities and verifying fixes through re-testing.

---

## 🛡️ Vulnerability Analysis and Implemented Remediation

### 1. SQL Injection (SQLi)

* **Vulnerability:** Direct string formatting (f-string) in the `SELECT` query using the `q` URL parameter.
* **Exploit:** The `' OR 1=1 --` payload bypassed the logic condition, causing a leak of all database records.
* **Remediation:** Using parameterized queries (*Prepared Statements*) with the `?` placeholder, separating SQL code from user data.

### 2. Stored Cross-Site Scripting (Stored XSS)

* **Vulnerability:** Rendering unsanitized database data using `innerHTML` in the DOM tree.
* **Exploit:** Injecting the `<img src="x" onerror="alert(1)">` payload, which was permanently stored in the database and executed on every page load.
* **Remediation:** Replacing it with the `.textContent` property, forcing the input to be treated strictly as a safe text literal.

### 3. Remote Command Injection (RCE)

* **Vulnerability:** Passing an IP address to a diagnostic tool with the `shell=True` parameter in the `subprocess` module.
* **Exploit:** The `127.0.0.1; cat /etc/passwd` payload allowed escaping the application context and reading sensitive system files.
* **Remediation:** Validating input using a character whitelist (Regex) and calling the binary process directly with an argument list (`shell=False`).

---

## 🚀 Running the Project Locally

```bash
# 1. Database initialization
python backend/init_db.py

# 2. Starting the Flask backend
python backend/app.py

```
