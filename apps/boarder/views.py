from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Board

# Create your views here.

class BoardListView(ListView):
    model = Board
    template_name = 'boarder/board_list.html'
    context_object_name = 'boards'
    paginate_by = 10

class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    template_name = 'boarder/board_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('boarder:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BoardDetailView(DetailView):
    model = Board
    template_name = 'boarder/board_detail.html'

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj

class BoardUpdateView(LoginRequiredMixin, UpdateView):
    model = Board
    template_name = 'boarder/board_form.html'
    fields = ['title', 'content']
    
    def get_success_url(self):
        return reverse_lazy('boarder:detail', kwargs={'pk': self.object.pk})

class BoardDeleteView(LoginRequiredMixin, DeleteView):
    model = Board
    success_url = reverse_lazy('boarder:list')
