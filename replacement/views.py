from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, FormView, UpdateView, CreateView, TemplateView, DeleteView, \
    DetailView
from django.contrib import messages

from replacement.forms import ReplacementForm, HardwareForm
from replacement.models import Hardware
from replacement.utils import RedirectToCorrectBrandMixin


class HomePageTemplateView(LoginRequiredMixin, TemplateView):
    """Login requierd view for home page.
    Displays the homepage for logged-in users.
    """
    template_name = "replacement_home_page_template_view.html"

    def get_context_data(self, **kwargs):
        """
        Adds the user's username to the context for display on the page.

        :param kwargs: Additional context arguments passed to the method.
        :return: Context with the user's username.
        """
        context = super().get_context_data(**kwargs)
        context["user_name"] = self.request.user.username

        return context


# ***********************************
# Hardware views
# ***********************************

class HardwareDetailListingView(LoginRequiredMixin, DetailView):
    """Login required view for hardware detail page.
    Displays detailed information about a specific hardware item.
    """
    template_name = "hardware_detail_view_page_template.html"
    model = Hardware
    context_object_name = "hardware"

    def get_context_data(self, **kwargs):
        """
        Adds the user's username to the context for display on the page.

        :param kwargs: Additional context arguments passed to the method.
        :return: Context with the user's username.
        """
        context = super().get_context_data(**kwargs)

        return context


class HardwareUpdateView(LoginRequiredMixin, RedirectToCorrectBrandMixin, UpdateView):
    """Login required view for hardware update page.
    After submmiting, redirects to correct brand listing page.
    """
    template_name = "hardware_update_view_page_template.html"
    model = Hardware
    context_object_name = "hardware"
    form_class = HardwareForm
    access_rights = ["editor"]

    def form_valid(self, form):
        """
        Displays a success message when the hardware update is submitted successfully.

        :param form: The form with valid data to update the hardware.
        :return: Redirects to the success URL after form validation.
        """
        messages.success(self.request, f"Stroj byl úspěšně upraven")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Adds the user's username to the context for display on the page.

        :param kwargs: Additional context arguments passed to the method.
        :return: Context with the user's username.
        """
        context = super().get_context_data(**kwargs)
        context["user_name"] = self.request.user.username

        return context



class HardwareCreateView(LoginRequiredMixin, RedirectToCorrectBrandMixin, CreateView):
    """Login required view for creating hardware page.
    After submmiting, redirects to correct brand listing page.
    """
    template_name = "hardware_create_view_page_template.html"
    model = Hardware
    context_object_name = "hardware"
    form_class = HardwareForm
    access_rights = ["editor"]

    def form_valid(self, form):
        """Displays a success message when the new hardware is created successfully.

        :param form: The form with valid data to create new hardware.
        :return: Redirects to the success URL after form validation.
        """
        messages.success(self.request, f"Nový stroj byl úspěšně přidán")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        """
        Adds the user's username to the context for display on the page.

        :param kwargs: Additional context arguments passed to the method.
        :return: Context with the user's username.
        """
        context = super().get_context_data(**kwargs)
        context["user_name"] = self.request.user.username

        return context

class HardwareDeleteView(LoginRequiredMixin, RedirectToCorrectBrandMixin, DeleteView):
    """Login required view for deleting hardware page.
    After submmiting, redirects to correct brand listing page
    """
    template_name = "hardware_delete_view_page_template.html"
    model = Hardware
    context_object_name = "hardware"
    access_rights = ["editor"]

    def form_valid(self, form):
        """Displays a success message when the hardware is successfully deleted.

        :param form: The form for hardware deletion.
        :return: Redirects to the success URL after deletion.
        """
        messages.success(self.request, f"Stroj byl úspěšně vymazán")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        """
        Adds the user's username to the context for display on the page.

        :param kwargs: Additional context arguments passed to the method.
        :return: Context with the user's username.
        """
        context = super().get_context_data(**kwargs)
        context["user_name"] = self.request.user.username

        return context

class ReplacementCalculationView(LoginRequiredMixin, FormView):
    """Login required view for calculating if HW needs to be replaced."""
    template_name = 'replacement_calculation_form_page_template.html'
    model = Hardware
    form_class = ReplacementForm
    access_rights = ["editor"]

    def get_context_data(self, **kwargs):
        """
        Adds the hardware details to the context for the replacement calculation.

        :param kwargs: Additional context arguments passed to the method.
        :return: Context with the hardware data to be used in the calculation.
        """
        context = super().get_context_data(**kwargs)

        hardware_id = self.kwargs.get('pk') # Get hardware ID from URL
        context['hardware'] = get_object_or_404(Hardware, pk=hardware_id) # Fetch hardware by ID
        print(context)
        return context

    def form_valid(self, form):
        """
        Performs the replacement calculation based on the input form data.

        :param form: The form containing user input for the calculation.
        :return: Renders the response with the calculation result.
        """
        hardware_id = self.kwargs.get('pk')
        hardware = get_object_or_404(Hardware, pk=hardware_id)

        replacement_calculation, message = form.calculate(hardware) # Perform the calculation

        context = self.get_context_data(form=form)
        context['replacement_calculation'] = replacement_calculation
        context['message'] = message # Add the calculation result and message to context
        print(message)
        return self.render_to_response(context) # Render the result




# ***********************************
# Brand listing views
# ***********************************


class KfcListingView(LoginRequiredMixin, ListView):
    """Brand listing view, shows Hw of KFC"""
    template_name = "kfc_listing_view_page_template.html"
    model = Hardware
    context_object_name = "hardware"
    access_rights = ["editor"]

    def get_queryset(self):
        """
        Filters and returns hardware items for the KFC brand.

        :return: Queryset of hardware for KFC and order by hw_name alphabetically.
        """
        return Hardware.objects.filter(brand_name__brand_name="KFC").order_by("hw_name")

    def get_context_data(self, **kwargs):
        """
        Adds the user's username to the context for display on the page.

        :param kwargs: Additional context arguments passed to the method.
        :return: Context with the user's username.
        """
        context = super().get_context_data(**kwargs)
        context["user_name"] = self.request.user.username

        return context

class StarbucksListingView(LoginRequiredMixin, ListView):
    """Brand listing view, shows Hw of Starbucks"""
    template_name = "starbucks_listing_view_page_template.html"
    model = Hardware
    context_object_name = "hardware"
    access_rights = ["editor"]

    def get_queryset(self):
        """
        Filters and returns hardware items for the Starbucks brand.

        :return: Queryset of hardware for Starbucks and order by hw_name alphabetically.
        """
        return Hardware.objects.filter(brand_name__brand_name="Starbucks").order_by("hw_name")

    def get_context_data(self, **kwargs):
        """
        Adds the user's username to the context for display on the page.

        :param kwargs: Additional context arguments passed to the method.
        :return: Context with the user's username.
        """
        context = super().get_context_data(**kwargs)
        context["user_name"] = self.request.user.username

        return context

class BurgerkingListingView(LoginRequiredMixin, ListView):
    """Brand listing view, shows Hw of Burger King"""
    template_name = "burger_king_listing_view_page_template.html"
    model = Hardware
    context_object_name = "hardware"
    access_rights = ["editor"]
    brand_name = "Burger King"

    def get_queryset(self):
        """
        Filters and returns hardware items for the Burger King brand.

        :return: Queryset of hardware for Burger King and order by hw_name alphabetically.
        """
        return Hardware.objects.filter(brand_name__brand_name="Burger King").order_by("hw_name")

    def get_context_data(self, **kwargs):
        """
        Adds the user's username to the context for display on the page.

        :param kwargs: Additional context arguments passed to the method.
        :return: Context with the user's username.
        """
        context = super().get_context_data(**kwargs)
        context["user_name"] = self.request.user.username

        return context

class PizzahutListingView(LoginRequiredMixin, ListView):
    """Brand listing view, shows Hw of Pizza Hut"""
    template_name = "pizza_hut_listing_view_page_template.html"
    model = Hardware
    context_object_name = "hardware"
    access_rights = ["editor"]

    def get_queryset(self):
        """
        Filters and returns hardware items for the Pizza Hut brand.

        :return: Queryset of hardware for Pizza Hut and order by hw_name alphabetically.
        """

        return Hardware.objects.filter(brand_name__brand_name="Pizza hut").order_by("hw_name")

    def get_context_data(self, **kwargs):
        """
        Adds the user's username to the context for display on the page.

        :param kwargs: Additional context arguments passed to the method.
        :return: Context with the user's username.
        """
        context = super().get_context_data(**kwargs)
        context["user_name"] = self.request.user.username

        return context