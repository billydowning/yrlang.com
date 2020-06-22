from django.forms import ModelForm, Form
from django import forms
from .models import BlogPostPage

class CreatePostForm(ModelForm):

	class Meta:
		model=BlogPostPage
		fields=["title","content"]