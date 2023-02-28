def processTemp(kelvin):
	celsius = kelvin-273.15
	farenheit = (celsius * 9/5)+32
	return str(round(celsius, 2))+"°C | "+str(round(farenheit, 2))+"°F | "+str(round(kelvin,2))+"K"
