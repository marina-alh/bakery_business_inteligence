# Production and sales Data analysis 
# Input: cvs files with production and sales data
# Output: 
#       1 - production growth by product


library(tidyverse)
library(ggplot2)
library(RODBC)

# LOCAL ODBC CONNECTION

con <- odbcConnect("PZ_operacao")

odbcCloseAll()

# reading tables into dfs

sqlTables(con)$TABLE_NAME

production <- sqlFetch(con, "PRODUCAO")
outsale <- sqlFetch(con, "VENDA_PADEIRO")
all_outsale <- sqlFetch(con,"VENDA_PADEIRO_TOTAL")
insale_M <- sqlFetch(con, "VENDA_BALCAO_M")
price <- sqlFetch(con, "PRECO")
insale_E <- sqlFetch(con, "VENDA_BALCAO_T")
all_sales <- sqlFetch(con,"VENDAS_TOTAL")


#PLOTS

# production vs sales
avg = all_sales %>% 
        summarise(pão_dagua=mean(D_P)+mean(D_G*4), pão_sovado = mean(S_P)+mean(S_G*4)) %>% 
        gather("PRODUTO","MEDIA_VENDAS")
          
        
ggplot(avg,aes(x = PRODUTO, y = MEDIA_VENDAS, fill = PRODUTO)) +
        geom_bar(stat="identity", width = 0.5) +
        theme_minimal() 
 
 
 
         


# comparação pão sovado e d'agua



# production vs sale by product





# total income










