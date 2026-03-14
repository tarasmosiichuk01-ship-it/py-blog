from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from blog.forms import CommentaryForm
from blog.models import Post


def index(request: HttpRequest) -> HttpResponse:
    post_list = Post.objects.all().order_by("-created_time")
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "post_list": page_obj,
    }
    return render(request, "blog/index.html", context=context)


class PostDetailView(generic.DetailView):
    model = Post
    form_class = CommentaryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentaryForm()
        context["commentaries"] = self.object.commentaries.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentaryForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                comment = form.save(commit=False)
                comment.post = self.object
                comment.user = request.user
                comment.save()
                return redirect("blog:post-detail", self.object.pk)
            else:
                form.add_error("content", "You must be logged in to comment")
                return render(
                    request,
                    "blog/post_detail.html",
                    context={
                        "form": form,
                        "object": self.object,
                        "commentaries": self.object.commentaries.all()
                    }
                )
        else:
            return render(
                request,
                "blog/post_detail.html",
                context={
                    "form": form,
                    "object": self.object,
                    "commentaries": self.object.commentaries.all()
                }
            )
