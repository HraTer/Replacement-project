from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, RedirectView

from replacement.utils import is_member_of_group


class HomePageRedirectView(RedirectView):
    """Redirects the user to the home page."""
    pattern_name = 'replacement:home-page'

    def get_redirect_url(self):
        """
        Returns the URL to redirect the user to.

        :return: Redirect URL.
        """
        return reverse_lazy(self.pattern_name)

# ***********************************
# Login/Logout process
# ***********************************

class AccountLoginView(FormView):
    """Displays the login form and processes user login."""
    template_name = "account_login_page_template.html"
    form_class = AuthenticationForm # hotovy form

    def form_valid(self, form):
        """
        Validates the login form, authenticates the user, and logs them in.

        :param form: Validated login form data.
        :return: Redirects to login confirmation if successful, or processes form again.
        """
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        # # Authenticate the user with the provided credentials.
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)   # Authenticate the user with the provided credentials.
            return HttpResponseRedirect(reverse_lazy("login-confirmation"))

        return super().form_valid(form)    # If unsuccessful, process the form again.


class AccountLoginConfirmationView(TemplateView):
    """Displays confirmation after successful login."""
    template_name = "account_login_confirmation_template.html"

class AccountLogoutView(RedirectView):
    """Logs the user out and redirects to a logout confirmation page."""
    url = reverse_lazy("logout-confirmation")

    logged_out_user = None

    def get(self, request, *args, **kwargs):
        """
        Logs the user out by removing their session and token.

        :param request: The HTTP request object.
        :return: Redirect to the logout confirmation page.
        """
        self.logged_out_user = request.user
        logout(request)
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        """
        Constructs the URL for the logout confirmation page, passing the user ID.

        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        :return: Logout confirmation URL with user ID.
        """
        user_pk = self.logged_out_user.pk if self.logged_out_user else ""
        return self.url + f"?userid={user_pk}"

class AccountLogoutYesNoView(TemplateView):
    """Displays a confirmation page asking the user if they want to log out."""
    template_name = "account_logout_yes_no_view.html"

class AccountLogoutConfirmationView(TemplateView):
    """Displays a confirmation page after the user logs out."""
    template_name = "account_logout_confirmation_template.html"

    def get_context_data(self, **kwargs):
        """
        Adds the logged-out user to the context for display on the logout confirmation page.

        :param kwargs: Additional context arguments passed to the method.
        :return: Context with the logged-out user's information.
        """
        context = super().get_context_data(**kwargs)
        user_pk = self.request.GET.get("userid")
        if user_pk:
            context["logged_in_user"] = User.objects.filter(pk=int(user_pk)).first()
        return context

class UserRightsMixin:
    """Mixin to check if the user belongs to a specific group with the required rights."""
    access_rights = []

    def user_has_rights(self, user):
        """
        Checks if the user belongs to the specified group(s).

        :param user: The user to check.
        :return: True if the user has the required rights, False otherwise.
        """
        return is_member_of_group(user, self.access_rights)

    def get_context_rights(self):
        """
        Adds user rights information to the context.

        :return: Context with user rights information.
        """
        context = {
            "user_has_rights": self.user_has_rights(self.request.user),
        }
        return context