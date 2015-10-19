from django.http import JsonResponse


def custom404(request):
    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    })
