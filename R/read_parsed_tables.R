library(data.table)

d = fread("output/BP_2024_Auvergne-Rhone-Alpes_v2.csv")
d1 = fread("output/BP_2024_Bretagne_v2.csv")

files = dir("output/")
files_csv = files[endsWith(files, ".csv")]

x = files_csv[1]
list_tabs = lapply(files_csv, \(x) fread(here::here("output", x)))

tab = rbindlist(list_tabs)
fwrite(tab, "BP_recap_regs_v1.csv")

d[, total_budget := as.numeric(total_budget)]

imp = fread("BP_recap_regs_v1.csv")