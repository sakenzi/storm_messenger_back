from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    photo = Column(Text, default="")
    online = Column(Boolean, default=False)
    last_visit = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_typing = Column(Boolean, default=False)  
    password = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    chats = relationship("Chat",primaryjoin="or_(User.id==Chat.user1_id, User.id==Chat.user2_id)")
    messages = relationship("Message", back_populates="sender")
    sent_requests = relationship("FriendRequest", foreign_keys='FriendRequest.from_user_id', back_populates="from_user")
    received_requests = relationship("FriendRequest", foreign_keys='FriendRequest.to_user_id', back_populates="to_user")


class FriendRequest(Base):
    __tablename__ = "friend_requests"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    to_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('from_user_id', 'to_user_id', name='uq_friend_request'),
    )

    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_requests")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_requests")

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user2_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="chat")
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages")
    media = relationship("MessageMedia", back_populates="message")  


class MediaType(Base):
    __tablename__ = "media_types"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String(20), nullable=False)

    message_media = relationship("MessageMedia", back_populates="media_type")


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    photo_url = Column(Text, nullable=False)


class Audio(Base):
    __tablename__ = "audios"

    id = Column(Integer, primary_key=True, index=True)
    audio_url = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)  


class Video(Base):
    __tablename__ = "videos"  

    id = Column(Integer, primary_key=True, index=True)
    video_url = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)  


class MessageMedia(Base):
    __tablename__ = "message_media"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    media_type_id = Column(Integer, ForeignKey("media_types.id"), nullable=False)
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=True)
    audio_id = Column(Integer, ForeignKey("audios.id"), nullable=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    message = relationship("Message", back_populates="media")
    media_type = relationship("MediaType", back_populates="message_media")
    photo = relationship("Photo")
    audio = relationship("Audio")
    video = relationship("Video")
