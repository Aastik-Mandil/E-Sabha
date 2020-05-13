from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponseRedirect
from rest_framework import viewsets

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView

from social.models import MyProfile
from social.models import MyPost
from social.models import PostComment
from social.models import PostLike
from social.models import FollowUser
from django.contrib.auth.models import User

from social.myserializer import MyProfileSerializer
from social.myserializer import MyPostSerializer
from social.myserializer import PostCommentSerializer
from social.myserializer import PostLikeSerializer
from social.myserializer import FollowUserSerializer
from social.myserializer import UserSerializer

@method_decorator(login_required, name="dispatch")
class HomeView(TemplateView):
    template_name = "social/home.html"
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        followedList = FollowUser.objects.filter(followed_by=self.request.user.myprofile)
        followedList2 = []
        for e in followedList:
            followedList2.append(e.profile)
        si = self.request.GET.get("si")
        if si==None:
            si=""
        postList =  MyPost.objects.filter(Q(uploaded_by__in=followedList2)).filter(Q(subject__icontains=si) | Q(msg__icontains=si)).order_by("-id");
        # postList = MyPost.objects.all()
        for p1 in postList:
            p1.com = []
            ob = PostComment.objects.filter(post=p1)
            if ob:
                for c in ob:
                    p1.com.append(c)
        for p1 in postList:
            p1.liked = False
            ob = PostLike.objects.filter(post=p1, liked_by=self.request.user.myprofile)
            if ob:
                p1.liked = True
            ob = PostLike.objects.filter(post=p1)
            p1.likecount = ob.count()
        for p1 in postList:
            p1.commented = False
            ob = PostComment.objects.filter(post=p1, commented_by=self.request.user.myprofile)
            if ob:
                p1.commented = True
            ob = PostComment.objects.filter(post=p1)
            p1.commentcount = ob.count()
        context["mypost_list"] = postList
        return context

class AboutView(TemplateView):
    template_name = "social/about.html"

class ContactView(TemplateView):
    template_name = "social/contact.html"

def follow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by=req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/myprofile")

def unfollow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by=req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/myprofile")

def like(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by=req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/home")

def unlike(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by=req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/home")

@method_decorator(login_required, name="dispatch")
class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ["name", "age", "address", "status", "gender", "phone_no", "description", "pic"]

@method_decorator(login_required, name="dispatch")
class MyPostCreate(CreateView):
    model = MyPost
    fields = ["subject", "msg", "pic"]
    def form_valid(self, form):
        self.object = form.save()
        # followedList = FollowUser.objects.filter(followed_by=self.request.user.myprofile)
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name="dispatch")
class MyPostListView(ListView):
    model = MyPost
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si==None:
            si=""
        return MyPost.objects.filter(Q(uploaded_by=self.request.user.myprofile)).filter(Q(subject__icontains=si) | Q(msg__icontains=si)).order_by("-id")

@method_decorator(login_required, name="dispatch")
class MyPostDetailView(DetailView):
    model = MyPost

@method_decorator(login_required, name="dispatch")
class MyPostDeleteView(DeleteView):
    model = MyPost

@method_decorator(login_required, name="dispatch")
class MyProfileListView(ListView):
    model = MyProfile
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si==None:
            si=""
        profList =  MyProfile.objects.filter(Q(name__icontains=si) | Q(address__icontains=si) | Q(gender__icontains=si) | Q(status__icontains=si)).order_by("-id")
        for p1 in profList:
            p1.followed = False
            ob = FollowUser.objects.filter(profile=p1, followed_by=self.request.user.myprofile)
            if ob:
                p1.followed = True
        return profList

@method_decorator(login_required, name="dispatch")
class MyProfileDetailView(DetailView):
    model = MyProfile

@method_decorator(login_required, name="dispatch")
class PostCommentCreate(CreateView):
    model = PostComment
    fields = ["post", "msg", "flag"]
    def form_valid(self, form):
        self.object = form.save()
        self.object.commented_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name="dispatch")
class PostCommenteListView(TemplateView):
    template_name = "social/postcomment_list.html"
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        followedList = FollowUser.objects.filter(followed_by=self.request.user.myprofile)
        followedList2 = []
        for e in followedList:
            followedList2.append(e.profile)
        si = self.request.GET.get("si")
        if si==None:
            si=""
        postList = MyPost.objects.filter(Q(uploaded_by__in=followedList2)).filter(Q(subject__icontains=si) | Q(msg__icontains=si)).order_by("-id")
        for p1 in postList:
            p1.com = []
            ob = PostComment.objects.filter(post=p1, commented_by=self.request.user.myprofile)
            if ob:
                for c in ob:
                    p1.com.append(c)
        # for p1 in postList:
        #     p1.liked = False
        #     ob = PostLike.objects.filter(post=p1, liked_by=self.request.user.myprofile)
        #     if ob:
        #         p1.liked = True
        #     ob = PostLike.objects.filter(post=p1)
        #     p1.likecount = ob.count()
        # for p1 in postList:
        #     p1.commented = False
        #     ob = PostComment.objects.filter(post=p1, commented_by=self.request.user.myprofile)
        #     if ob:
        #         p1.commented = True
        #     ob = PostComment.objects.filter(post=p1)
        #     p1.commentcount = ob.count()
        context["mypost_list"] = postList
        return context

# api
@method_decorator(login_required, name="dispatch")
class MyProfileViewSet(viewsets.ModelViewSet):
    queryset = MyProfile.objects.all().order_by("-id")
    serializer_class = MyProfileSerializer

@method_decorator(login_required, name="dispatch")
class MyPostViewSet(viewsets.ModelViewSet):
    queryset = MyPost.objects.all().order_by("-id")
    serializer_class = MyPostSerializer

@method_decorator(login_required, name="dispatch")
class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all().order_by("-id")
    serializer_class = PostCommentSerializer

@method_decorator(login_required, name="dispatch")
class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all().order_by("-id")
    serializer_class = PostLikeSerializer

@method_decorator(login_required, name="dispatch")
class FollowUserViewSet(viewsets.ModelViewSet):
    queryset = FollowUser.objects.all().order_by("-id")
    serializer_class = FollowUserSerializer

@method_decorator(login_required, name="dispatch")
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer