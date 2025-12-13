# Demo Test Users - MWECAU ICT Club

This document lists sample users for testing the MWECAU ICT Club platform across different user levels and roles.

---

## 📋 User Levels Overview

The system supports the following user levels based on course/program level:

- **CERT** - Certificate Level (1 year)
- **DIP** - Diploma Level (2 years)
- **DEG** - Bachelor Degree Level (3 years)
- **MASTER** - Master Degree Level (2 years)
- **PHD** - Doctor of Philosophy Level (3 years)

---

## 👥 Sample Test Users

### 1. **Certificate Level - Non-Staff User**

| Field | Value |
|-------|-------|
| **Username** | T/CERT/2025/001 |
| **Registration Number** | T/CERT/2025/001 |
| **Email** | cert.student@mwecau.ac.tz |
| **Password** | CertPass123!Demo |
| **Full Name** | Grace Mwenyake Kipchoge |
| **Course** | Certificate in Information Technology |
| **Department** | Networking |
| **Status** | Pending Approval |
| **Role** | Regular Member |

**Create Command:**
```bash
python manage.py create_test_user \
  --email cert.student@mwecau.ac.tz \
  --password "CertPass123!Demo" \
  --dept Networking \
  --regnumber T/CERT/2025/001 \
  --fullname "Grace Mwenyake Kipchoge"
```

---

### 2. **Diploma Level - Non-Staff User (Approved)**

| Field | Value |
|-------|-------|
| **Username** | T/DIP/2024/005 |
| **Registration Number** | T/DIP/2024/005 |
| **Email** | dip.student@mwecau.ac.tz |
| **Password** | DipPass456!Demo |
| **Full Name** | Samuel Mwangi Kariuki |
| **Course** | Diploma in Computer Science |
| **Department** | Programming |
| **Status** | Approved |
| **Role** | Regular Member |

**Create Command:**
```bash
python manage.py create_test_user \
  --email dip.student@mwecau.ac.tz \
  --password "DipPass456!Demo" \
  --dept Programming \
  --regnumber T/DIP/2024/005 \
  --fullname "Samuel Mwangi Kariuki" \
  --approved
```

---

### 3. **Bachelor Degree Level - Non-Staff User (Approved)**

| Field | Value |
|-------|-------|
| **Username** | T/DEG/2025/001 |
| **Registration Number** | T/DEG/2025/001 |
| **Email** | john.doe@mwecau.ac.tz |
| **Password** | StrongPass123! |
| **Full Name** | John Doe Smith |
| **Course** | Bachelor of Science in Computer Science |
| **Department** | Programming |
| **Status** | Approved |
| **Role** | Regular Member |

**Create Command:**
```bash
python manage.py create_test_user \
  --email john.doe@mwecau.ac.tz \
  --password "StrongPass123!" \
  --dept Programming \
  --regnumber T/DEG/2025/001 \
  --fullname "John Doe Smith" \
  --approved
```

---

### 4. **Bachelor Degree Level - Staff User (Admin)**

| Field | Value |
|-------|-------|
| **Username** | T/DEG/2023/100 |
| **Registration Number** | T/DEG/2023/100 |
| **Email** | admin@mwecau.ac.tz |
| **Password** | AdminPass789!Secure |
| **Full Name** | Dr. Michael Admin Mwakalila |
| **Course** | Bachelor of Science in Computer Science |
| **Department** | Programming |
| **Status** | Approved |
| **Role** | System Administrator |

**Create Command:**
```bash
python manage.py create_test_user \
  --email admin@mwecau.ac.tz \
  --password "AdminPass789!Secure" \
  --dept Programming \
  --regnumber T/DEG/2023/100 \
  --fullname "Dr. Michael Admin Mwakalila" \
  --approved \
  --isstaff
```

---

### 5. **Master Degree Level - Non-Staff User (Approved)**

| Field | Value |
|-------|-------|
| **Username** | T/MASTER/2024/001 |
| **Registration Number** | T/MASTER/2024/001 |
| **Email** | mary.m@mwecau.ac.tz |
| **Password** | SecurePass456@ |
| **Full Name** | Mary Mwendo Mushi |
| **Course** | Master of Business Administration |
| **Department** | Cybersecurity |
| **Status** | Approved |
| **Role** | Regular Member (Postgraduate) |

**Create Command:**
```bash
python manage.py create_test_user \
  --email mary.m@mwecau.ac.tz \
  --password "SecurePass456@" \
  --dept Cybersecurity \
  --regnumber T/MASTER/2024/001 \
  --fullname "Mary Mwendo Mushi" \
  --course "Master of Business Administration" \
  --approved
```

---

### 6. **Master Degree Level - Staff User (Department Leader)**

| Field | Value |
|-------|-------|
| **Username** | T/MASTER/2023/050 |
| **Registration Number** | T/MASTER/2023/050 |
| **Email** | leader@mwecau.ac.tz |
| **Password** | LeaderPass999!Admin |
| **Full Name** | Prof. Daniel Kipchoge Leader |
| **Course** | Master of Science with Education |
| **Department** | AI & Machine Learning |
| **Status** | Approved |
| **Role** | Department Leader + Admin |

**Create Command:**
```bash
python manage.py create_test_user \
  --email leader@mwecau.ac.tz \
  --password "LeaderPass999!Admin" \
  --dept "AI & Machine Learning" \
  --regnumber T/MASTER/2023/050 \
  --fullname "Prof. Daniel Kipchoge Leader" \
  --course "Master of Science with Education" \
  --approved \
  --isstaff
```

---

### 7. **PhD Level - Non-Staff User (Pending)**

| Field | Value |
|-------|-------|
| **Username** | T/PHD/2023/001 |
| **Registration Number** | T/PHD/2023/001 |
| **Email** | phd.researcher@mwecau.ac.tz |
| **Password** | PhDPass111!Research |
| **Full Name** | Dr. Alexander Kipchoge Kariuki |
| **Course** | Doctor of Philosophy in Education |
| **Department** | AI & Machine Learning |
| **Status** | Pending Approval |
| **Role** | Research Scholar |

**Create Command:**
```bash
python manage.py create_test_user \
  --email phd.researcher@mwecau.ac.tz \
  --password "PhDPass111!Research" \
  --dept "AI & Machine Learning" \
  --regnumber T/PHD/2023/001 \
  --fullname "Dr. Alexander Kipchoge Kariuki" \
  --course "Doctor of Philosophy in Education"
```

---

## 🚀 Quick Setup - Create All Demo Users

Run all commands to populate the database with demo users:

```bash
cd src

# Certificate Level
python manage.py create_test_user \
  --email cert.student@mwecau.ac.tz \
  --password "CertPass123!Demo" \
  --dept Networking \
  --regnumber T/CERT/2025/001 \
  --fullname "Grace Mwenyake Kipchoge"

# Diploma Level
python manage.py create_test_user \
  --email dip.student@mwecau.ac.tz \
  --password "DipPass456!Demo" \
  --dept Programming \
  --regnumber T/DIP/2024/005 \
  --fullname "Samuel Mwangi Kariuki" \
  --approved

# Bachelor Degree - Regular User
python manage.py create_test_user \
  --email john.doe@mwecau.ac.tz \
  --password "StrongPass123!" \
  --dept Programming \
  --regnumber T/DEG/2025/001 \
  --fullname "John Doe Smith" \
  --approved

# Bachelor Degree - Admin
python manage.py create_test_user \
  --email admin@mwecau.ac.tz \
  --password "AdminPass789!Secure" \
  --dept Programming \
  --regnumber T/DEG/2023/100 \
  --fullname "Dr. Michael Admin Mwakalila" \
  --approved \
  --isstaff

# Master Degree - Regular User
python manage.py create_test_user \
  --email mary.m@mwecau.ac.tz \
  --password "SecurePass456@" \
  --dept Cybersecurity \
  --regnumber T/MASTER/2024/001 \
  --fullname "Mary Mwendo Mushi" \
  --course "Master of Business Administration" \
  --approved

# Master Degree - Department Leader
python manage.py create_test_user \
  --email leader@mwecau.ac.tz \
  --password "LeaderPass999!Admin" \
  --dept "AI & Machine Learning" \
  --regnumber T/MASTER/2023/050 \
  --fullname "Prof. Daniel Kipchoge Leader" \
  --course "Master of Science with Education" \
  --approved \
  --isstaff

# PhD Level
python manage.py create_test_user \
  --email phd.researcher@mwecau.ac.tz \
  --password "PhDPass111!Research" \
  --dept "AI & Machine Learning" \
  --regnumber T/PHD/2023/001 \
  --fullname "Dr. Alexander Kipchoge Kariuki" \
  --course "Doctor of Philosophy in Education"
```

---

## 🔐 User Authentication

All users can login using their **Registration Number** as the username:

**Example Login Credentials:**

```
Username: T/DEG/2025/001
Password: StrongPass123!
```

---

## 📊 User Status Summary

| Level | Username | Email | Approved | Staff | Course |
|-------|----------|-------|----------|-------|--------|
| CERT | T/CERT/2025/001 | cert.student@mwecau.ac.tz | ❌ | ❌ | Certificate in IT |
| DIP | T/DIP/2024/005 | dip.student@mwecau.ac.tz | ✅ | ❌ | Diploma in CS |
| DEG | T/DEG/2025/001 | john.doe@mwecau.ac.tz | ✅ | ❌ | BS Computer Science |
| DEG | T/DEG/2023/100 | admin@mwecau.ac.tz | ✅ | ✅ | BS Computer Science |
| MASTER | T/MASTER/2024/001 | mary.m@mwecau.ac.tz | ✅ | ❌ | Master of Business Admin |
| MASTER | T/MASTER/2023/050 | leader@mwecau.ac.tz | ✅ | ✅ | Master of Science + Education |
| PHD | T/PHD/2023/001 | phd.researcher@mwecau.ac.tz | ❌ | ❌ | Doctor of Philosophy in Education |

---

## 🧪 Testing Workflow

1. **Register New User** → Use CERT or PHD users (status: Pending)
2. **Approve User** → Admin user can approve pending registrations
3. **Access Member Portal** → Login with approved users
4. **Upload Picture** → Users have 72 hours to upload profile picture
5. **View Dashboard** → Access personalized member dashboard
6. **Admin Functions** → Use admin/staff accounts for management tasks

---

## 📝 Notes

- All passwords meet strength requirements: 8+ chars, uppercase, lowercase, digit, special character
- Registration numbers follow format: `T/[LEVEL]/[YEAR]/[NUMBER]`
- Users can be created without approval for testing registration workflow
- Staff users have admin capabilities for management functions
- Department assignment is mandatory for all users
- Course assignment is optional (can be added later)

---

**Last Updated:** December 13, 2025
**System Version:** 1.0 (108 commits)
