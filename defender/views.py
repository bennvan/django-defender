from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import admin

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from .utils import get_blocked_ips, get_blocked_usernames, unblock_ip, unblock_username


@user_passes_test(lambda u: u.has_perm('defender.change_accessattempt'))
def block_view(request):
    context = admin.site.each_context(request)
    """ List the blocked IP and Usernames """
    blocked_ip_list = get_blocked_ips()
    blocked_username_list = get_blocked_usernames()

    context.update({
        "blocked_ip_list": blocked_ip_list,
        "blocked_username_list": blocked_username_list,
    })
    return render(request, "defender/admin/blocks.html", context)


@user_passes_test(lambda u: u.has_perm('defender.change_accessattempt'))
def unblock_ip_view(request, ip_address):
    """ upblock the given ip """
    if request.method == "POST":
        unblock_ip(ip_address)
    return HttpResponseRedirect(reverse("defender_blocks_view"))


@user_passes_test(lambda u: u.has_perm('defender.change_accessattempt'))
def unblock_username_view(request, username):
    """ unblockt he given username """
    if request.method == "POST":
        unblock_username(username)
    return HttpResponseRedirect(reverse("defender_blocks_view"))
