from django.views.generic.base import TemplateView


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        user = context.get("user")
        profile_image_url = None
        try:
            profile_image_url = user.socialaccount_set.all()[0].get_avatar_url()
            context["user"].profile_image_url = profile_image_url
        except Exception:
            pass
        return context
