from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required


@login_required
def new_conversation(request, item_pk):
    item :Item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('item:detail', item_id=item.pk)
    
    conversation = Conversation.objects.filter(item=item).filter(members__in=[request.user.pk])

    if conversation:
        return redirect('conversation:detail', conversation_pk=conversation.first().pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()
            
            conversation_message : ConversationMessage  = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', item_id=item.pk)
    else:
        form = ConversationMessageForm()
    
    return render(request, 'conversation/new.html', {
        'form': form,
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.pk])
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })


def detail(request, conversation_pk):
    conversation = Conversation.objects.filter(members__in=[request.user.pk]).get(pk=conversation_pk)
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation_message : ConversationMessage  = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            return redirect('conversation:detail', conversation_pk=conversation.pk)
        
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form,
    })