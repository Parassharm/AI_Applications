from flask import Flask, render_template, request

app = Flask(__name__)

units_by_category = {
    "Length": {
        "meter": "Meter",
        "kilometer": "Kilometer",
        "mile": "Mile",
        "yard": "Yard",
        "foot": "Foot",
        "inch": "Inch"
    },
    "Weight": {
        "kilogram": "Kilogram",
        "gram": "Gram",
        "milligram": "Milligram",
        "pound": "Pound",
        "ounce": "Ounce"
    },
    "Temperature": {
        "celsius": "Celsius",
        "fahrenheit": "Fahrenheit",
        "kelvin": "Kelvin"
    }
}

conversion_factors = {
    "Length": {
        "meter": 1,
        "kilometer": 1000,
        "mile": 1609.34,
        "yard": 0.9144,
        "foot": 0.3048,
        "inch": 0.0254
    },
    "Weight": {
        "kilogram": 1,
        "gram": 0.001,
        "milligram": 0.000001,
        "pound": 0.453592,
        "ounce": 0.0283495
    }
}

def convert_units(category, value, from_unit, to_unit):
    if category == "Temperature":
        if from_unit == to_unit:
            return value
        if from_unit == "celsius":
            if to_unit == "fahrenheit":
                return (value * 9 / 5) + 32
            elif to_unit == "kelvin":
                return value + 273.15
        elif from_unit == "fahrenheit":
            if to_unit == "celsius":
                return (value - 32) * 5 / 9
            elif to_unit == "kelvin":
                return (value - 32) * 5 / 9 + 273.15
        elif from_unit == "kelvin":
            if to_unit == "celsius":
                return value - 273.15
            elif to_unit == "fahrenheit":
                return (value - 273.15) * 9 / 5 + 32
        return None
    else:
        try:
            value_in_base = value * conversion_factors[category][from_unit]
            return value_in_base / conversion_factors[category][to_unit]
        except KeyError:
            return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    selected_category = 'Length'

    if request.method == 'POST':
        selected_category = request.form['category']
        from_unit = request.form['from_unit']
        to_unit = request.form['to_unit']
        value = float(request.form['value'])
        result = convert_units(selected_category, value, from_unit, to_unit)

    return render_template(
        'index.html',
        categories=units_by_category.keys(),
        units=units_by_category,
        selected_category=selected_category,
        result=result
    )

if __name__ == '__main__':
    app.run(debug=True)
