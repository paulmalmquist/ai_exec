from app.db.database import SessionLocal
from app.adapters.seed import seed_clients, seed_risks, seed_resources, seed_templates


def main():
    db = SessionLocal()
    seed_clients(db)
    seed_risks(db)
    seed_resources(db)
    seed_templates(db)


if __name__ == "__main__":
    main()
