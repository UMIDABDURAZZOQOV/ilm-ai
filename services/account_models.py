"""Additive deletion state; created only by the explicit lifecycle migration."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from services.models import User

AccountBase = declarative_base()


class DeletionChallenge(AccountBase):
    __tablename__ = "account_deletion_challenges"
    id = Column(String(64), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)
    email_hash = Column(String(64), nullable=False, index=True)
    code_hash = Column(String(64), nullable=False)
    attempts = Column(Integer, nullable=False, default=0)
    consumed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)


class DeletionJob(AccountBase):
    __tablename__ = "account_deletion_jobs"
    id = Column(String(64), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    state = Column(String(32), nullable=False)
    email_hash = Column(String(64), nullable=True)  # HMAC; cleared after file purge
    created_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class DeletionRateBucket(AccountBase):
    __tablename__ = "account_deletion_rate_buckets"
    key_hash = Column(String(64), primary_key=True)
    count = Column(Integer, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
