# Arcpy-Kernel
Código Python para metodologia de aplicação do Kernel Density e Zonal Statistics. 

 - Este código foi produzido durante meu periodo de estagio no ICMBio.
 - Não criei a metodologia, porém o codigo foi feito no Arcpy e atualizado no ArcGis Pro por mim. 
 - Recomendo conhecimento basico em SIG e Python, quando eu estava criando utilizei o ModelBuilder, uma otima ferramenta para seguir a metodologia. 

🔧 Requisitos
  - ArcGIS Pro instalado com licença para Spatial Analyst e Image Analyst (necessário para usar arcpy.sa e arcpy.ia).

  - Python com a biblioteca arcpy (instalado junto com o ArcGIS Pro).

  - Permissões adequadas para ler e escrever dados em diretórios do projeto.

📥 Entradas
   - O script usa 6 parâmetros de entrada, que são definidos ao rodar o script via ArcGIS Pro ou uma ferramenta personalizada:

   - input_features – Camada vetorial com os dados de produção (com campo de ano).

   - select_year – Ano a ser filtrado (ex: 2024).

   - input_limites – Limites geográficos para aplicar o kernel e estatísticas zonais.

   - output – Caminho do raster de saída final.

   - input_uc – Camada de Unidades de Conservação (UCs) para calcular estatísticas finais.

   - tabela – Tabela de saída com as estatísticas zonais por UC.

⚙️ O que o script faz
   - Filtra os dados de produção com base no ano escolhido.

   - Calcula área em hectares e gera pontos a partir dos polígonos.

   - Gera dois rasters de densidade:

   - Um ponderado pela área (area_ha);

   - Outro sem peso.

   - Normaliza ambos os rasters com estatísticas mínimas e máximas por zona.

   - Calcula a média dos dois resultados normalizados.

   - Salva o raster final.

   - Gera uma tabela com estatísticas zonais para cada Unidade de Conservação.

📌 Observações
   - As operações são realizadas temporariamente na memória (memory\\), o que melhora performance, mas exige que o ArcGIS esteja configurado corretamente.

   - Os parâmetros de Kernel Density são adaptáveis. Os valores utilizados foram:

     - search_radius: 0.0015 (em unidades do sistema de referência da camada);

     - cell_size: 0.77713003870646 (ajustar conforme o projeto).

   - É importante que os dados estejam com geometrias válidas – o script usa RepairGeometry para garantir isso.

📌 Observações
   - As operações são realizadas temporariamente na memória (memory\\), o que melhora performance, mas exige que o ArcGIS esteja configurado corretamente.

   - Os parâmetros de Kernel Density são adaptáveis. Os valores utilizados foram:

   - search_radius: 0.0015 (em unidades do sistema de referência da camada);

   - cell_size: 0.77713003870646 (ajustar conforme o projeto).

   - É importante que os dados estejam com geometrias válidas – o script usa RepairGeometry para garantir isso.

🤝 Créditos
Este código foi desenvolvido durante meu estágio no ICMBio, com base em uma metodologia pré-existente. A automação via Arcpy foi realizada por mim, com apoio do meu supervisor Juan orozco.

