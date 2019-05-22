# sensors & displays

## devices prêts :)

### BH1750 (Lux)

+ test OK, ca mesure en lux, ca marche bien!

### VL53L0X (laser/distance)

+ a priori OK, mais à tester
+ voir aussi ça: https://forum.micropython.org/viewtopic.php?f=14&t=6440

### CCS811 (Qair, CO)

+ a priori OK, à tester:
  + https://github.com/Notthemarsian/CCS811

### MCP9808 (t°)

+ a priori OK, à tester:
  + https://github.com/kfricke/micropython-mcp9808

## devices pas prêts :(

### BME680 (Qair, hygro, t°, pression)

+ pas d'implémentation en micropython
+ à faire, à partir de la librairie Arduino, par exemple, et des specs
  - https://github.com/SV-Zanshin/BME680/blob/master/src/Zanshin_BME680.cpp 
  - https://www.mouser.com/datasheet/2/783/BST-BME680-DS001-00-1221303.pdf
