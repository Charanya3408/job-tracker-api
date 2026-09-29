"""Fill the dev database with sample applications for test1@example.com."""
from datetime import date, timedelta

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import Application, Status, User

SAMPLE = [
    ("Zoho", "Software Developer", "linkedin", Status.interview, 30),
    ("Freshworks", "Backend Engineer", "referral", Status.offer, 28),
    ("Infosys", "Systems Engineer", "portal", Status.rejected, 27),
    ("TCS", "Digital Analyst", "portal", Status.applied, 25),
    ("Razorpay", "SDE Intern", "linkedin", Status.oa, 22),
    ("Swiggy", "Data Analyst Intern", "linkedin", Status.rejected, 21),
    ("Zomato", "ML Intern", "linkedin", Status.applied, 18),
    ("PhonePe", "SDE Intern", "referral", Status.interview, 15),
    ("Cred", "Backend Intern", "linkedin", Status.applied, 12),
    ("Wipro", "Project Engineer", "portal", Status.applied, 10),
    ("Postman", "Software Engineer", "referral", Status.oa, 8),
    ("Groww", "Data Engineer Intern", "linkedin", Status.rejected, 6),
    ("Meesho", "SDE Intern", "portal", Status.applied, 3),
    ("Atlassian", "Graduate Engineer", "linkedin", Status.applied, 1),
]


def main():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == "test1@example.com"))
        if user is None:
            raise SystemExit("Register test1@example.com first.")
        for company, role, source, status, days_ago in SAMPLE:
            db.add(
                Application(
                    user_id=user.id,
                    company=company,
                    role=role,
                    source=source,
                    status=status,
                    applied_on=date.today() - timedelta(days=days_ago),
                )
            )
        db.commit()
        print(f"Seeded {len(SAMPLE)} applications.")


if __name__ == "__main__":
    main()
