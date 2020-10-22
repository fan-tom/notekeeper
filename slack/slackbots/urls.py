"""slackbots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from common.router import Router
from common.views import SlackHook
from core.processors import NoteKeeper
from notekeeper.commands_deserializers import TopWrapper, PushWrapper
from notekeeper.note_repo_impl import NoteRepoImpl

urlpatterns = [
    # TODO: probably, it is wrong place to configure router and command processor
    path('slackhook/', SlackHook.as_view(router=Router(
        dict(notekeeper=NoteKeeper(NoteRepoImpl())),
        dict(push=PushWrapper, top=TopWrapper)
    ))),
    path('notekeeper/', include('notekeeper.urls'))
]
