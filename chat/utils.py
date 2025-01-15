from dataclasses import dataclass

import ollama
from django.db.models import F
from django.db.models import QuerySet
from pgvector.django import L2Distance

from transport.models import TransportationData
from transport.utils import generate_embedding


@dataclass
class TransportationMetrics:
  district: str
  green_transport: float
  public_transport: float
  non_motorized: float
  walking: float
  bike: float
  private_motorized: float
  most_used_public_transport: float

  def format_metrics(self) -> str:
    """Format transportation metrics into a readable string."""
    return (
      f"{self.district}: ["
      f"綠運輸:{self.green_transport}%, "
      f"公共運具:{self.public_transport}%, "
      f"非機動運具:{self.non_motorized}%, "
      f"步行:{self.walking}%, "
      f"自行車(含公共):{self.bike}%, "
      f"私人機動運具:{self.private_motorized}%, "
      f"最常公共運具使用率:{self.most_used_public_transport}%"
      f"]"
    )


def get_nearest_transportation_data(query_vector: list, top_k: int) -> QuerySet:
  """Retrieve the nearest transportation data based on vector similarity."""
  return TransportationData.objects.annotate(
      distance=L2Distance(F("embedding"), query_vector)
  ).order_by("distance")[:top_k]


def retrieve_context(query: str, top_k: int = 13) -> str:
  """
  Retrieve and format context related to user input using vector database.

  Args:
      query: User input query string
      top_k: Number of results to return (default: 13)

  Returns:
      Formatted string containing transportation metrics for nearest matches
  """
  query_vector = generate_embedding(query)
  results = get_nearest_transportation_data(query_vector, top_k)

  transportation_metrics = [
    TransportationMetrics(
        district=result.district,
        green_transport=result.green_transport,
        public_transport=result.public_transport,
        non_motorized=result.non_motorized,
        walking=result.walking,
        bike=result.bike,
        private_motorized=result.private_motorized,
        most_used_public_transport=result.most_used_public_transport
    ) for result in results
  ]

  return "\n".join(metric.format_metrics() for metric in transportation_metrics)


def generate_response(user_message: str, memory: list):
  """
  將用戶輸入、檢索的上下文和記憶傳送給 ollama/llama3.2 模型，返回 AI 回覆。
  """
  # 檢索上下文
  context = retrieve_context(user_message)

  # 修正聊天歷史處理
  history = []
  for msg in memory:
    if "user" in msg:
      history.append({"role": "user", "content": msg["user"]})
    if "bot" in msg:
      history.append({"role": "assistant", "content": msg["bot"]})

  # 添加當前上下文和用戶輸入
  messages = [
    {"role": "system",
     "content": f"請遵循下列資訊："
                f"1.開頭請自稱「交通小小助理」並使用貼心、溫暖的方式進行回覆，除了專業用語與程式碼之外，請使用繁體中文回覆。\n"
                f"2.如果提問內容無法對應到 context的內容，請反問使用者「請提供更明確的問題？」。 \n"
                f"3.全區指的是臺北市，臺北市中的資訊是其下12個行政區的平均值。 \n"
                f"Use the following context for the conversation:"
                f"\n{context}"},
    *history,
    {"role": "user", "content": user_message}
  ]
  print("MSG: " + str(messages))

  # 調用 ollama/llama3.2
  try:
    response = ollama.chat(model="llama3.2", messages=messages)
    # 確保 response 是字典格式
    bot_response = response.get("message", {}).get("content",
                                                   "抱歉，我無法回答這個問題。")
    print("BOT: " + str(bot_response))
  except Exception as e:
    bot_response = f"Error occurred: {str(e)}"

  return bot_response, context
