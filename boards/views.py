from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import redirect


# Create your views here.


def board_list(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    products = Board.objects.all()

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    return render(request, 'board/list.html', {'current_category': current_category,
                                               'categories': categories, 'products': products})


class BoardUploadView(CreateView):
    model = Board
    fields = [
        'photo', 'text', 'date', 'category'
    ]
    template_name = 'board/upload.html'

    def form_valid(self, form):
        form.instance.authors_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/boards')
        else:
            return self.render_to_response({'form': form})


class BoardDeleteView(DeleteView):
    model = Board
    success_url = '/boards'
    template_name = 'board/delete.html'


class BoardUpdateView(UpdateView):
    model = Board
    fields = ['photo', 'text', 'date', 'category']
    template_name = 'board/update.html'
    success_url = '/boards'


class BoardDetailView(DetailView):
    model = Board
    template_name = 'board/detail.html'
