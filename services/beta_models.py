from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base
from services.models import User

BetaBase = declarative_base()


class BetaTestIdentity(BetaBase):
    __tablename__ = 'beta_test_identities'
    # Only a hash of the device-generated 256-bit credential is stored.
    credential_hash = Column(String(64), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
