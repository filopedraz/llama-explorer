from django.contrib import admin

from sources.models import Commit, GithubUser, Repository


class GithubUserAdmin(admin.ModelAdmin):
    list_display = ("login", "name", "location", "company", "email", "twitter_username")


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ("name", "stars", "language")


class CommitAdmin(admin.ModelAdmin):
    list_display = ("sha", "developer", "repository")


admin.site.register(GithubUser, GithubUserAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Commit, CommitAdmin)
