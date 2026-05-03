from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from shop_chat.forms import ChatUserCreationForm


@login_required
@require_http_methods(["GET"])
def chat_index_page(request, room_name):
    """
    Відображає сторінку конкретної чат-кімнати за її назвою.
    Доступ дозволено лише авторизованим користувачам.
    """
    # В будущем здесь стоит добавить: room = get_object_or_404(Room, name=room_name)
    return render(request, 'chat_room.html', {'room_name': room_name})


@require_http_methods(["GET", "POST"])
def register(request):
    """
    Обробляє реєстрацію нових користувачів чату.
    При GET-запиті повертає форму реєстрації.
    При POST-запиті створює користувача, виконує вхід та перенаправляє до чату.
    """
    if request.method == 'POST':
        form = ChatUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat_page', room_name='initial_room')
    else:
        form = ChatUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})