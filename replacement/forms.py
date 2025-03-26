from django import forms
from django.core.exceptions import ValidationError

import replacement
from replacement.models import Hardware
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ReplacementForm(forms.ModelForm):
    """
    Form for calculating whether hardware should be replaced.
    Includes fields for repair offer, service cost, and hardware production date.
    """
    repair_offer = forms.DecimalField(label='Cenová nabídka', max_digits=10, decimal_places=2, help_text="Zadej cenovou nabídku na opravu")
    service_cost = forms.DecimalField(label='Částka za opravy', max_digits=10, decimal_places=2, help_text="Zadej kolik stály minulé opravy")
    hw_production_date = forms.DateField(
        label='Výrobní datum',
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        help_text="Zadej datum výroby stroje"
    )

    class Meta:
        model = Hardware
        fields = ['repair_offer', 'service_cost', 'hw_production_date']

    def clean_hw_production_date(self):
        """
        Validates the production date to ensure it is in the past.

        :raises ValidationError: If the production date is in the future.
        :return: Cleaned hardware production date.
        """
        hw_production_date = self.cleaned_data.get('hw_production_date')
        today = datetime.today().date()

        if isinstance(hw_production_date, datetime):
            hw_production_date = hw_production_date.date()

        # Ensure the production date is not in the future.
        if hw_production_date > today:
            raise ValidationError("Datum výroby musí být v minulosti.")

        return hw_production_date


    def calculate(self, hardware):
        """
        Performs the replacement calculation based on the hardware's age, repair costs, and other factors.

        :param hardware: Hardware instance used for calculations.
        :return: Tuple containing the replacement calculation value and the corresponding message.
        """
        # Calculate the age of the hardware in months
        today = datetime.today().date()
        hw_production_date = self.cleaned_data['hw_production_date']

        if isinstance(hw_production_date, datetime):
            hw_production_date = hw_production_date.date()

        hardware_age = relativedelta(today, hw_production_date).years * 12 + relativedelta(today,
                                                                                           hw_production_date).months

        # Calculate the residual value of the hardware
        write_off_length = hardware.write_off_length
        remaining_months = max(0, write_off_length * 12 - hardware_age)
        residual_value = float((remaining_months / (write_off_length * 12)) * hardware.hw_price)

        # Gather other necessary values
        repair_offer = float(self.cleaned_data['repair_offer'])
        service_cost = float(self.cleaned_data['service_cost'])

        # Perform the replacement equation
        ers = repair_offer + service_cost
        kpc = hardware.hw_price * 0.2
        tbo = 0 if hardware_age < 60 else (hardware_age - 60) / 3
        ezh = ((residual_value + 1) / hardware.hw_price) * 100
        replacement_calculation = int(((ers - kpc) / 1000) + tbo - ezh)


        rounded_replacement_calculation = round(replacement_calculation, 2)

        print(rounded_replacement_calculation)

        # Final message for the user based on the replacement calculation
        if rounded_replacement_calculation > 10:
            message = f"Replacement proběhne, oprava je nákladná. Výsledek rovnice je {rounded_replacement_calculation}."
        elif -10 < rounded_replacement_calculation < 10:
            message = f"Je to na individuálním posouzení, výsledek rovnice je {rounded_replacement_calculation}."
        else:
            message = f"Replacement neproběhne, zařízení je buďto nové nebo je oprava výhodná. Výsledek rovnice je {rounded_replacement_calculation}."

        # Return the replacement calculation and message
        return replacement_calculation, message

class HardwareForm(forms.ModelForm):
    """
    Form for creating or updating hardware data.
    Includes fields for brand name, hardware name, price, and write-off length.
    """
    class Meta:
        model = Hardware
        fields = ['brand_name', 'hw_name', 'hw_price', 'write_off_length']

        labels = {
            "brand_name": "Brand",
            "hw_name": "Název zařízení",
            "hw_price": "Pořizovací cena zařízení",
            "write_off_length": "Doba odpisu zařízení",
        }

        help_texts = {
            "brand_name": "Zadejte brand",
            "hw_name": "Zadejte název zařízení",
            "hw_price": "Zadejte cenu zařízení",
            "write_off_length": "Zadejte dobu odpisu v letech"
        }

    def clean_write_off_length(self):
        """
        Validates the write-off period to ensure it is one of the allowed values (3, 5, or 7 years).

        :raises ValidationError: If the write-off length is not 3, 5, or 7 years.
        :return: Cleaned write-off length.
        """
        write_off_length = self.cleaned_data.get('write_off_length')

        # Ensure the write-off length is either 0, 3, 5, or 7 years
        if write_off_length not in [0, 3, 5, 7]:
            raise ValidationError("Délka odpisu musí být 0, 3, 5 nebo 7 let.")

        return write_off_length

