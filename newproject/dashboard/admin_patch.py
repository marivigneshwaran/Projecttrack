from django.contrib import admin

from .context import get_dashboard_context


def apply_admin_dashboard():
    site = admin.site
    if getattr(site, '_dashboard_patched', False):
        return

    original_index = site.index

    # def index(request, extra_context=None):
    #     context = extra_context or {}
    #     context.update(get_dashboard_context())
    #     return original_index(request, context)

    def index(request, extra_context=None):
        context = extra_context or {}
        context.update(get_dashboard_context(request))  # Pass the request down
        return original_index(request, context)

    site.index = index
    site._dashboard_patched = True
