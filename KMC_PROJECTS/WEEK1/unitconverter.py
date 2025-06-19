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


def convert_units(category, value, from_unit, to_unit): #in function definition, the items inside the bracket are parameters
            value_in_base = value * conversion_factors[category][from_unit] #converts the value in base unit value ie. either in metres or in kilograms
            return value_in_base / conversion_factors[category][to_unit] #converts the base unit value into required unit.



category = input("enter category:")
val = float(input("Enter value:")) #changes string to float
fromUnit = input("Enter the given unit:")
toUnit = input("enter your desired unit:")


answer = round(convert_units(category, val, fromUnit, toUnit),2)
print("Value converted from "+ str(val)+fromUnit+ " to " +str(answer)+ toUnit)
