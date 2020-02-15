from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import redirect

# Create your views here.


class BoardList(ListView):
    template_name = 'secondboard/list.html'

    def get_queryset(self):
        if self.kwargs:
            self.categories = Category.objects.all()
            self.current_category = get_object_or_404(
                Category, slug=self.kwargs.get('category_slug'))
            self.products = Board.objects.filter(
                category=self.current_category)
        else:
            self.current_category = None
            self.categories = Category.objects.all()
            self.products = Board.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_category'] = self.current_category
        context['categories'] = self.categories
        context['products'] = self.products
        return context


class BoardUploadView(CreateView):
    model = Board
    fields = [
        'photo', 'text', 'date', 'category'
    ]
    template_name = 'secondboard/upload.html'

    def form_valid(self, form):
        form.instance.authors_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/secondboards')
        else:
            return self.render_to_response({'form': form})


class BoardDeleteView(DeleteView):
    model = Board
    success_url = '/secondboards'
    template_name = 'secondboard/delete.html'


class BoardUpdateView(UpdateView):
    model = Board
    fields = ['photo', 'text', 'date', 'category']
    template_name = 'secondboard/update.html'
    success_url = '/secondboards'


class BoardDetailView(DetailView):
    model = Board
    template_name = 'secondboard/detail.html'
