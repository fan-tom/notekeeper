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

from common.Router import Router
from common.views import SlackHook
from core.commands import Push, Top
from core.processors import NoteKeeper
from notekeeper.note_repo_impl import NoteRepoImpl

urlpatterns = [
    # TODO: probably, it is wrong place to configure router and command processor
    path('slackhook/', SlackHook.as_view(router=Router(
        dict(notekeeper=NoteKeeper(NoteRepoImpl())),
        dict(push=Push, top=Top)
    ))),
    path('notekeeper/', include('notekeeper.urls'))
]
