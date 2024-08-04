from datetime import datetime


def convert_date_format(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError('Invalid date format. It must be in MM/DD/YYYY format.')
