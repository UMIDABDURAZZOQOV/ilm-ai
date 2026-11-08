"""Purpose-bound deletion proofs, separate from ordinary OAuth/login grants."""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from services.models import User
from services.account_models import DeletionChallenge

ReauthBase = declarative_base()


class DeletionReauth(ReauthBase):
    __tablename__ = "account_deletion_reauth"
    state_hash = Column(String(64), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)
    method = Column(String(16), nullable=False)
    surface = Column(String(16), nullable=False)
    phase = Column(String(16), nullable=False)
    nonce_hash = Column(String(64), nullable=True)
    challenge = Column(String(43), nullable=True)
    identity_hash = Column(String(64), nullable=True)
    grant_hash = Column(String(64), nullable=True, unique=True)
    challenge_id = Column(
        String(64), ForeignKey(DeletionChallenge.id), nullable=True, unique=True
    )
    created_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    exchange_expires_at = Column(DateTime(timezone=True), nullable=True)


class ManualDeletionRequest(ReauthBase):
    __tablename__ = "account_deletion_manual_requests"
    id = Column(String(43), primary_key=True)
    account_hash = Column(String(64), nullable=False)
    contact_hash = Column(String(64), nullable=False)
    encrypted_details = Column(Text, nullable=False)
    state = Column(String(32), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
