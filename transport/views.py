from django.http import JsonResponse

from .utils import parse_and_store_md


def load_md_to_db(request):
  try:
    parse_and_store_md()
    return JsonResponse(
        {"status": "success", "message": "Data loaded into the database."})
  except Exception as e:
    return JsonResponse({"status": "error", "message": str(e)}, status=500)
