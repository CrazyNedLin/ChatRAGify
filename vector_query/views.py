import json

from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pgvector.django import L2Distance

from transport.models import TransportationData
from transport.utils import generate_embedding


@csrf_exempt
def vector_search(request):
  """
  查詢向量資料庫，返回與輸入文本最相似的記錄，接收 JSON 格式的查詢。
  """
  if request.method == "POST":
    try:
      # 確保 Content-Type 是 application/json
      if request.content_type != "application/json":
        return JsonResponse({"error": "Content-Type must be application/json"},
                            status=400)

      # 解析 JSON 請求
      data = json.loads(request.body)
      query_text = data.get("query")

      if not query_text:
        return JsonResponse({"error": "Query text is required"}, status=400)

      # 生成查詢文本的嵌入向量
      query_vector = generate_embedding(query_text)

      # 使用 L2Distance 計算相似度，返回最接近的記錄
      results = TransportationData.objects.annotate(
          distance=L2Distance(F("embedding"), query_vector)
      ).order_by("distance")[:3]  # 取前 5 筆相似記錄

      # 組裝回應資料
      response_data = [
        {
          "district": result.district,
          "green_transport": result.green_transport,
          "public_transport": result.public_transport,
          "non_motorized": result.non_motorized,
          "walking": result.walking,
          "bike": result.bike,
          "private_motorized": result.private_motorized,
          "most_used_public_transport": result.most_used_public_transport,
          "distance": result.distance,
        }
        for result in results
      ]

      return JsonResponse({"results": response_data}, status=200)

    except json.JSONDecodeError:
      return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)

  return JsonResponse({"error": "Invalid request method"}, status=405)
