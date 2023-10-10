
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from .models import Item, Category
from .forms import NewItemForm, EditItemForm

# Create your views here.


#  ----------------------- VIEW ONE ITEM ------------------
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

#  ----------------------- VIEW ITEMS ------------------
def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id: 
        items = items.filter(category_id=category_id)

    if query:
        # The 'Q' comes from django and lets us search in the name or description of the item
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query) )

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

#  ----------------------- CREATE ITEM ------------------
# Must be logged in to create new item
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            # creates item but doesn't save yet
            item = form.save(commit=False)
            # Links logged in user to created_by FK
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    # if not post must be GET request
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item',
    })

#  ----------------------- DELETE ITEM ------------------

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')

#  ----------------------- Edit ITEM ------------------
@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)
    # if not post must be GET request
    else:
        # fill form with instace info
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item',
    })