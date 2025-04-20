from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item, Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm
from django.http import HttpRequest
from django.db.models import Q


def items(request : HttpRequest):
    search_query = request.GET.get('query', '')
    category_id = request.GET.get('category', -1)
    items = Item.objects.filter(is_sold=False).order_by('-created_at')
    categories = Category.objects.all()

    if category_id != -1:
        items = items.filter(category_id=category_id)
 
    if search_query:
        items = items.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    context = {
        'items': items,
        'query': search_query,
        'categories': categories,
        'category_id': int(category_id),
    }
    return render(request, 'item/items.html', context)


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
            item : Item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', item_id=item.id)
    else:
        form = NewItemForm()
    
    return render(request, 'item/form.html', {'form': form})

@login_required
def edit(request, item_id):
    item : Item = get_object_or_404(Item, id=item_id, created_by=request.user)
    
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail', item_id=item.id)
    else:
        form = EditItemForm(instance=item)
    
    return render(request, 'item/form.html', {'form': form})    


@login_required
def delete(request, item_id):
    item : Item = get_object_or_404(Item, id=item_id, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')