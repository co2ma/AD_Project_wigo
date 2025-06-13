from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def receive_post(request):
    name = request.data.get('name')
    message = request.data.get('message')
    if not name or not message:
        return Response(
            {"error": "name과 message는 필수입니다."},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"result": f"{name}님이 보낸 메시지: {message}"},
        status=status.HTTP_201_CREATED
    ) 