
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
	user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
	phone_number = models.CharField(max_length=20, null=True, blank=True)
	role = models.CharField(max_length=10, choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')], default='guest')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.username} ({self.email})"

class Conversation(models.Model):
	conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
	participants = models.ManyToManyField(User, related_name='conversations')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Conversation {self.conversation_id}"

class Message(models.Model):
	message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
	message_body = models.TextField()
	sent_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Message {self.message_id} from {self.sender}" 
