import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from chat.models import ChatRecord
from chat.utils import generate_response


@csrf_exempt
def chat_with_memory(request):
  """
  Chat API：處理用戶輸入，返回 AI 回覆，並記錄問答。
  """
  if request.method == "POST":
    try:
      data = json.loads(request.body)
      user_message = data.get("message")

      if not user_message:
        return JsonResponse({"error": "Message is required"}, status=400)

      # 獲取最近 10 條問答記錄
      chat_history = ChatRecord.objects.order_by("-created_at")[:10]
      memory = [{"user": record.user_message, "bot": record.bot_response} for
                record in chat_history]

      # 生成回覆
      bot_response, context = generate_response(user_message, memory)

      # 存儲問答記錄
      ChatRecord.objects.create(
          user_message=user_message,
          bot_response=bot_response,
          context=context
      )

      return JsonResponse({"response": bot_response}, status=200)

    except json.JSONDecodeError:
      return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)

  return JsonResponse({"error": "Invalid request method"}, status=405)
