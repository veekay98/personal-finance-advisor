from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Expense

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add an expense
@router.post("/expenses")
def add_expense(category: str, amount: float, db: Session = Depends(get_db)):
    new_expense = Expense(category=category, amount=amount)
    db.add(new_expense)
    db.commit()
    return {"message": "Expense added!", "expense": {"category": category, "amount": amount}}

# Get all expenses
@router.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(Expense).all()
    return {"expenses": expenses}
