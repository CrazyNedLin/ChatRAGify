from django.db import models
from django.utils.timezone import now


class ChatRecord(models.Model):
  user_message = models.TextField()  # 用戶輸入的問題
  bot_response = models.TextField()  # AI 的回覆
  context = models.TextField()  # RAG 機制的上下文
  created_at = models.DateTimeField(default=now)  # 創建時間
