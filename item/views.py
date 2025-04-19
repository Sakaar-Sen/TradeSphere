from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm

# Create your views here.
def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=item_id)[:3]
    
    context = {
        'item': item,
        'related_items': related_items,
    }
    
    return render(request, 'item/detail.html', context)


@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('item:detail', item_id=item.id)
    else:
        form = NewItemForm()
    
    return render(request, 'item/new.html', {'form': form})