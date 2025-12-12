import json
from pathlib import Path
import csv

MOCK_RESULTS = [
    {"id": "reset_pw_001", "jtbd": "reset_password", "correct": True, "polite": True, "reply": "To reset your password, go to the login page and click 'Forgot Password'. Enter your email address and you'll receive a password reset link within 5 minutes."},
    {"id": "reset_pw_002", "jtbd": "reset_password", "correct": True, "polite": True, "reply": "Of course! Visit the login page, select 'Forgot Password', and follow the instructions sent to your registered email. The reset link is valid for 24 hours."},
    {"id": "reset_pw_003", "jtbd": "reset_password", "correct": True, "polite": True, "reply": "If you can't log in, click 'Forgot Password' on the login page. We'll send you a secure link to create a new password."},
    {"id": "reset_pw_004", "jtbd": "reset_password", "correct": True, "polite": True, "reply": "You can change your password directly in Account Settings. Log in, go to Security, and select 'Change Password'."},
    {"id": "register_course_001", "jtbd": "course_registration", "correct": True, "polite": True, "reply": "To register for CS101, log in to the student portal, go to 'Courses', find CS101, and click 'Enroll'. You'll need to confirm your registration."},
    {"id": "register_course_002", "jtbd": "course_registration", "correct": True, "polite": True, "reply": "Visit the Courses section in your student dashboard, search for 'Advanced Python', and click 'Register'. Confirmation will be instant."},
    {"id": "register_course_003", "jtbd": "course_registration", "correct": True, "polite": True, "reply": "Yes, you can register for multiple courses. Simply find each course in the Courses section and click 'Enroll' for each one."},
    {"id": "register_course_004", "jtbd": "course_registration", "correct": True, "polite": True, "reply": "If a course is full, you can join the waitlist by clicking 'Join Waitlist' on the course page."},
]

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Save JSONL
with open(RESULTS_DIR / "results_mock.jsonl", "w", encoding="utf-8") as f:
    for r in MOCK_RESULTS:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

# Save CSV
with open(RESULTS_DIR / "results_mock.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "jtbd", "correct", "polite", "reply"])
    writer.writeheader()
    for r in MOCK_RESULTS:
        writer.writerow(r)

# Print summary
total = len(MOCK_RESULTS)
passed = sum(1 for r in MOCK_RESULTS if r["correct"] and r["polite"])
print(f"\n=== MOCK EVAL SUMMARY ===")
print(f"Total: {total}")
print(f"Passed (correct & polite): {passed}/{total}")
print(f"Results saved to {RESULTS_DIR}/")