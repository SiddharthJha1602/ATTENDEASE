# Manual Test Cases

## TC01 - Valid Login

Precondition:
- User account exists

Steps:
1. Open login page
2. Enter valid username
3. Enter valid password
4. Click Login

Expected Result:
- User redirected to dashboard

---

## TC02 - Invalid Login

Steps:
1. Open login page
2. Enter invalid username/password
3. Click Login

Expected Result:
- Error message displayed

---

## TC03 - Empty Login

Steps:
1. Open login page
2. Leave fields blank
3. Click Login

Expected Result:
- Validation message displayed

---

## TC04 - Mark Attendance

Steps:
1. Login
2. Click Mark Attendance

Expected Result:
- Attendance recorded successfully

---

## TC05 - Duplicate Attendance

Steps:
1. Mark attendance once
2. Attempt to mark again

Expected Result:
- Duplicate attendance prevented

---

## TC06 - Apply Leave

Steps:
1. Login
2. Open Leave Page
3. Submit leave request

Expected Result:
- Leave request submitted

---

## TC07 - Leave Validation

Steps:
1. Leave mandatory fields empty
2. Submit form

Expected Result:
- Validation error displayed

---

## TC08 - View Leave Status

Steps:
1. Login
2. Open Leave Status

Expected Result:
- Leave status displayed

---

## TC09 - Logout

Steps:
1. Login
2. Click Logout

Expected Result:
- User redirected to Login page

---

## TC10 - Admin Leave Approval

Steps:
1. Login as Admin
2. Open Leave Requests
3. Approve leave

Expected Result:
- Leave status updated to Approved