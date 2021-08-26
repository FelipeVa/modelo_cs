\* Computer_Plant_Problem *\
Minimize
Costo_Total: 5 x_Denver_Barstow + 8 x_Denver_Dallas + 6 x_Denver_San_Diego
 + 3 x_Denver_Tucson + 3 x_Los_Angeles_Barstow + 6 x_Los_Angeles_Dallas
 + 5 x_Los_Angeles_San_Diego + 2 x_Los_Angeles_Tucson + 7 x_Phoenix_Barstow
 + 10 x_Phoenix_Dallas + 4 x_Phoenix_San_Diego + 8 x_Phoenix_Tucson
 + 8 x_San_Francisco_Barstow + 5 x_San_Francisco_Dallas
 + 9 x_San_Francisco_San_Diego + 6 x_San_Francisco_Tucson + 70000 y_Denver
 + 70000 y_Los_Angeles + 65000 y_Phoenix + 70000 y_San_Francisco
Subject To
Sum_of_Products_into_Stores_Barstow: x_Denver_Barstow + x_Los_Angeles_Barstow
 + x_Phoenix_Barstow + x_San_Francisco_Barstow >= 1000
Sum_of_Products_into_Stores_Dallas: x_Denver_Dallas + x_Los_Angeles_Dallas
 + x_Phoenix_Dallas + x_San_Francisco_Dallas >= 1200
Sum_of_Products_into_Stores_San_Diego: x_Denver_San_Diego
 + x_Los_Angeles_San_Diego + x_Phoenix_San_Diego + x_San_Francisco_San_Diego
 >= 1700
Sum_of_Products_into_Stores_Tucson: x_Denver_Tucson + x_Los_Angeles_Tucson
 + x_Phoenix_Tucson + x_San_Francisco_Tucson >= 1500
Sum_of_Products_out_of_Plant_Denver: x_Denver_Barstow + x_Denver_Dallas
 + x_Denver_San_Diego + x_Denver_Tucson - 2000 y_Denver <= 0
Sum_of_Products_out_of_Plant_Los_Angeles: x_Los_Angeles_Barstow
 + x_Los_Angeles_Dallas + x_Los_Angeles_San_Diego + x_Los_Angeles_Tucson
 - 2000 y_Los_Angeles <= 0
Sum_of_Products_out_of_Plant_Phoenix: x_Phoenix_Barstow + x_Phoenix_Dallas
 + x_Phoenix_San_Diego + x_Phoenix_Tucson - 1700 y_Phoenix <= 0
Sum_of_Products_out_of_Plant_San_Francisco: x_San_Francisco_Barstow
 + x_San_Francisco_Dallas + x_San_Francisco_San_Diego + x_San_Francisco_Tucson
 - 170 y_San_Francisco <= 0
Binaries
y_Denver
y_Los_Angeles
y_Phoenix
y_San_Francisco
End
