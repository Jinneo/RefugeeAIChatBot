from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import ChatForm
from .logic import chatbot_response

def create(request):
   return render(request, "chatbot/create_testbot.html")

class ChatView(View):
    template_name = 'chatbot/index.html'

    def get(self, request):
        form = ChatForm()

        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if not is_ajax:
            request.session['chat_history'] = []

        chat_history = request.session.get('chat_history', [])
        return render(request, self.template_name, {'form': form, 'chatbot_response': '', 'chat_history': chat_history})

    def post(self, request):
        form = ChatForm(request.POST)
        chat_history = request.session.get('chat_history', [])
        print("got here")

        # return render(request, self.template_name, {'form': form, 'chatbot_response': '', 'chat_history': chat_history})


        if form.is_valid():
            user_message = form.cleaned_data['message']
            if user_message.lower() == "exit":
                chat_history.append({'role': 'User', 'text': user_message})
                request.session['chat_history'] = chat_history
                return render(request, self.template_name, {'form': form, 'chatbot_response': 'Goodbye!', 'chat_history': chat_history})

            chatbot_response_text = chatbot_response(user_message)
            print(chatbot_response_text)
            chat_history.append({'role': 'User', 'text': user_message})

            if not chat_history or chatbot_response_text != chat_history[-1]['text']:
                chat_history.append({'role': 'Chatbot', 'text': chatbot_response_text})

            request.session['chat_history'] = chat_history

            return JsonResponse({'chatbot_response': chatbot_response_text})
        else:
            return render(request, self.template_name, {'form': form, 'chatbot_response': '', 'chat_history': chat_history})
