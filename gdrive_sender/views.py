
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .services import GoogleDriveService


@csrf_exempt
@require_POST
def create_file_view(request):
    if request.method == "POST":
        service = GoogleDriveService()

        file_name = request.POST.get("name")
        text_content = request.POST.get("data")

        if not (file_name and text_content):
            return JsonResponse(
                status=400, data={"message": "File name or data missing."}
            )
        if service.file_exists(file_name):
            return JsonResponse(
                status=400,
                data={"message": f"File with name {file_name} alredy exists."},
            )

        file_id = service.create_file(file_name, text_content)
        return JsonResponse(status=201, data={"message": {"fileID": file_id}})
