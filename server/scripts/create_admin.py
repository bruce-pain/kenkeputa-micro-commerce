import argparse
import sys
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from app.db.database import SessionLocal, init_db  # noqa: E402
from app.api.repositories.user import UserRepository  # noqa: E402
from app.api.models.user import User  # noqa: E402
from app.utils import password_utils  # noqa: E402

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Create or promote an admin user.")
    parser.add_argument("--email", required=True, help="Email for the admin user")
    parser.add_argument(
        "--password",
        required=False,
        help="Password for the admin user (required when creating)",
    )
    args = parser.parse_args()

    init_db()

    session = SessionLocal()
    try:
        repo = UserRepository(session)
        existing_user = repo.get_by_email(args.email)

        if existing_user:
            if existing_user.role == "admin":
                logger.info("%s is already an admin.", args.email)
                return
            existing_user.role = "admin"
            if args.password:
                existing_user.password = password_utils.hash_password(args.password)
            session.commit()
            session.refresh(existing_user)
            logger.info("Promoted %s to admin.", args.email)
        else:
            if not args.password:
                parser.error("Password is required when creating a new admin user.")
            hashed_password = password_utils.hash_password(args.password)
            admin_user = User(email=args.email, password=hashed_password, role="admin")
            repo.create(admin_user)
            logger.info("Created admin user %s.", args.email)
    finally:
        session.close()


if __name__ == "__main__":
    main()