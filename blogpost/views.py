# import code; code.interact(local=dict(globals(), **locals()))
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreatePostForm
from .models import BlogPostPage
from users.models import CustomUser
from django.views.generic import (CreateView, ListView, UpdateView, DeleteView)
from customemixing.session_and_login_mixing import UserSessionAndLoginCheckMixing


class PostCreateView(UserSessionAndLoginCheckMixing, CreateView):
    template_name = "create_post.html"
    form_class = CreatePostForm

    def form_valid(self, form):
        current_user = CustomUser.get(self.request.user.id)
        post = form.save(commit=False)
        post.user = current_user
        post.save()
        messages.success(self.request, "Your post has been created!")
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class PostView(UserSessionAndLoginCheckMixing, ListView):
    template_name = "post.html"
    context_object_name = 'post'

    def get_queryset(self):
        return BlogPostPage.objects.get(id=self.kwargs.get('post_id'))


class PostDelete(UserSessionAndLoginCheckMixing, UserPassesTestMixin, DeleteView):
    model = BlogPostPage
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if post.user == self.request.user:
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class PostUpdateView(UserSessionAndLoginCheckMixing, UserPassesTestMixin, UpdateView):
    template_name = "create_post.html"
    form_class = CreatePostForm
    model = BlogPostPage

    def test_func(self):
        post = self.get_object()
        if post.user == self.request.user:
            return True
        else:
            return False

    def form_valid(self, form):
        current_post = get_object_or_404(BlogPostPage, pk=self.kwargs.get('pk'))
        form.save()
        messages.success(self.request, "Your Post has been updated!")
        return redirect(reverse("post", args=[current_post.id]))

    def form_invalid(self, form):
        messages.error(self.request, "Your request couldn't be processed!")
        return self.render_to_response(self.get_context_data(form=form))
