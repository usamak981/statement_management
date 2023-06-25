from django.shortcuts import render, get_object_or_404, redirect
from .forms import SenderForm
from .models import Sender

def sender_list(request):
    senders = Sender.objects.all()
    return render(request, 'sender/index.html', {'senders': senders})

def sender_create(request):
    if request.method == 'POST':
        form = SenderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sender_list')
    else:
        form = SenderForm(None)
    return render(request, 'sender/create.html', {'form': form})

def sender_update(request, pk):
    sender = get_object_or_404(Sender, pk=pk)
    if request.method == 'POST':
        form = SenderForm(request.POST, instance=sender)
        if form.is_valid():
            form.save()
            return redirect('sender_list')
    else:
        form = SenderForm(instance=sender)
    return render(request, 'sender/create.html', {'form': form, 'sender': sender})

def sender_delete(request, pk):
    sender = get_object_or_404(Sender, pk=pk)
    # if request.method == 'POST':
    sender.delete()
    return redirect('sender_list')
    # return render(request, 'sender/sender_delete.html', {'sender': sender})
