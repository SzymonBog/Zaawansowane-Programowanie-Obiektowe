class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(temp):
        t = (temp * 1.8) + 32
        return t

    @staticmethod
    def fahrenheit_to_celsius(temp):
        t = (temp - 32) / 1.8
        return t


c = 20
f = TemperatureConverter.celsius_to_fahrenheit(c)
print(f)
c = TemperatureConverter.fahrenheit_to_celsius(f)
print(c)
