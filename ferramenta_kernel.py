# Bibliotecas
import arcpy
from arcpy.sa import *
import os

# Parâmetros de entrada
input_features = arcpy.GetParameterAsText(0)
select_year = arcpy.GetParameterAsText(1)
input_limites = arcpy.GetParameterAsText(2)
output = arcpy.GetParameterAsText(3)
input_uc = arcpy.GetParameterAsText(4)
tabela = arcpy.GetParameterAsText(5)

# Processamento
# filtrar o ano de 2024
prod = r'memory\prod'
ano = f"year = {float(select_year)}"

arcpy.analysis.Select(input_features, prod, ano)
arcpy.RepairGeometry_management(prod)

arcpy.management.CalculateGeometryAttributes(prod, [["area_ha", "AREA_GEODESIC"]], area_unit="HECTARES")
prod_point = r'memory\prod_point'
arcpy.management.FeatureToPoint(prod, prod_point)

# Kernel e Zonal com população (area_ha)
kernl_pop = r'memory\kernl_pop'
with arcpy.EnvManager(mask=input_limites):
    kernl_pop = arcpy.sa.KernelDensity(prod_point, "area_ha", "0.0015", "0.77713003870646", "SQUARE_MAP_UNITS",
                                       "DENSITIES", "PLANAR", "")

# Zonal statistics zona min e max
zonal_min = r'memomry\zonal_min'
Zonal_Statistics_2_ = zonal_min
zonal_min = arcpy.ia.ZonalStatistics(input_limites, "FID", kernl_pop, "MINIMUM", "DATA", "CURRENT_SLICE", 90,
                                     "AUTO_DETECT", "ARITHMETIC", 360)

zonal_max = r'memory\zonal_max'
Zonal_Statistics = zonal_max
zonal_max = arcpy.ia.ZonalStatistics(input_limites, "FID", kernl_pop, "MAXIMUM", "DATA", "CURRENT_SLICE", 90,
                                     "AUTO_DETECT", "ARITHMETIC", 360)

# Calculo com kernel pop
valor_pop = r'memory\valor_pop'
Raster_Calculator = valor_pop
valor_pop = (kernl_pop - zonal_min) / (zonal_max - zonal_min)

# Kernel e Zonal com população None
kernel_no_pop = r'memory\kernel_no_pop'
Kernel_Density_2_ = kernel_no_pop
with arcpy.EnvManager(mask=input_limites):
    kernel_no_pop = arcpy.sa.KernelDensity(prod_point, "NONE", "0,0015", "0,77713003870646", "SQUARE_MAP_UNITS",
                                           "DENSITIES", "PLANAR", "")

# Cálculo com kernel no pop

zonal_min_1 = r'memory\tifs\\zonal_min_1'
Zonal_Statistics_4_ = zonal_min_1
zonal_min_1 = arcpy.ia.ZonalStatistics(input_limites, "FID", kernel_no_pop, "MINIMUM", "DATA", "CURRENT_SLICE", 90,
                                       "AUTO_DETECT", "ARITHMETIC", 360)

zonal_max_1 = 'memory\zonal_max_1'
Zonal_Statistics_3_ = zonal_max_1
zonal_max_1 = arcpy.ia.ZonalStatistics(input_limites, "FID", kernel_no_pop, "MAXIMUM", "DATA", "CURRENT_SLICE", 90,
                                       "AUTO_DETECT", "ARITHMETIC", 360)

# Calculo com kernel no pop
valor_nopop = r'memory\valor_nopop'
Raster_Calculator_2_ = valor_nopop
valor_nopop = (kernel_no_pop - zonal_min_1) / (zonal_max_1 - zonal_min_1)

# Cálculo final
resultado = (valor_pop + valor_nopop) / 2
# resultado.save(output)

arcpy.management.CopyRaster(resultado, output)

uc = arcpy.management.CopyFeatures(input_uc, r'memory\uc')
arcpy.RepairGeometry_management(uc)

Output_Join_Layer = ""
arcpy.ia.ZonalStatisticsAsTable(uc, "Nome_UC", resultado, tabela, "DATA", "ALL", "CURRENT_SLICE", 90, "AUTO_DETECT",
                                "ARITHMETIC", 360, Output_Join_Layer)
