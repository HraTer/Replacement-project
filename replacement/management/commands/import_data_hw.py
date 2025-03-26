import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from replacement.models import Brand, Hardware  # Replace 'myapp' with your actual app name


class Command(BaseCommand):
    help = 'Imports hardware data from a CSV file'

    def handle(self, *args, **kwargs):
        # Specify the path to your CSV file
        file_path = '/Users/terezahrabalova/Desktop/Brands_data.xlsx - List1.csv'

        # Open the CSV file
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Clean the hw_price field by replacing non-breaking spaces and other unwanted characters
                brand_name = row.get('brand_name')
                hw_name = row.get('hw_name')

                # Strip any whitespace or non-breaking spaces in hw_price and convert it to an integer
                hw_price = row.get('hw_price', '0').replace('\xa0', '').replace(' ', '')
                hw_price = int(hw_price)  # Convert the cleaned string to integer

                write_off_length = int(row.get('write_off_length', 0))  # Default to 0 if missing
                hw_production_date = datetime.now()  # Assuming current date for production

                if not brand_name:
                    print("Missing brand_name in row:", row)
                    continue

                # Get or create the brand instance
                brand, created = Brand.objects.get_or_create(brand_name=brand_name)

                # Create the hardware entry
                Hardware.objects.create(
                    brand_name=brand,
                    hw_name=hw_name,
                    hw_price=hw_price,
                    write_off_length=write_off_length,
                    hw_production_date=hw_production_date
                )

            self.stdout.write(self.style.SUCCESS('Data imported successfully!'))