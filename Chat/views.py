from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage
from .serializers import ChatMessageSerializer
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from accounts.models import CustomUser

apiKey=settings.API_KEY #환경 변수

@method_decorator(csrf_exempt, name='dispatch')
class ChatView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        chat_history = ChatMessage.objects.filter(user=user).order_by('timestamp')
        serializer = ChatMessageSerializer(chat_history, many=True)
        return Response(serializer.data)

    def post(self, request, user_id, *args, **kwargs):
        try:
            user_message = request.body.decode('utf-8').strip()
        except UnicodeDecodeError:
            return Response({'error': 'Invalid request body'}, status=status.HTTP_400_BAD_REQUEST)

        if not user_message:
            return Response({'error': 'Message cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Save user message
        ChatMessage.objects.create(user=user, role='user', content=user_message)

        # Fetch previous messages for this user
        previous_messages = ChatMessage.objects.filter(user=user).order_by('timestamp')
        message_list = [{"role": msg.role, "content": msg.content} for msg in previous_messages]

        # Add system message
        message_list.append({
            "role": "system",
            "content": "How can I help you?"
        })

        # Make an HTTP request to the OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {apiKey}"},
            json={
                "model": "gpt-4",
                "messages": message_list
            }
        )

        if response.status_code != 200:
            return Response({'error': 'Failed to fetch response from OpenAI'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_json = response.json()
        assistant_response = response_json['choices'][0]['message']['content']

        # Save assistant message
        ChatMessage.objects.create(user=user, role='assistant', content=assistant_response)

        # Fetch updated chat history for this user
        updated_chat_history = ChatMessage.objects.filter(user=user).order_by('timestamp')
        serializer = ChatMessageSerializer(updated_chat_history, many=True)

        return Response({'response': assistant_response, 'chat_history': serializer.data}, status=status.HTTP_200_OK)
