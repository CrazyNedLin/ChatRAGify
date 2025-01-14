from django.http import JsonResponse

from .utils import parse_and_store_md, convert_image_to_markdown


def load_md_to_db(request):
  try:
    parse_and_store_md()
    return JsonResponse(
        {"status": "success", "message": "Data loaded into the database."})
  except Exception as e:
    return JsonResponse({"status": "error", "message": str(e)}, status=500)

def process_image_with_ollama(image_path):
  try:
    convert_image_to_markdown('../testinfo.png')
    return JsonResponse(
        {"status": "success", "message": "PNG convert to markdown."})
  except Exception as e:
    return JsonResponse({"status": "error", "message": str(e)}, status=500)
