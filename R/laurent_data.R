library(haven)

l = haven::read_dta('data/Laurent/RegDep20112025_Synthese.dta')
setDT(l)

reglong = l[coll == "Reg"] |> dplyr::select(-coll) |> melt(id.vars = c("Nom", "year"))

reglong[, variable := as.character(variable)]
reglong[, source := substr(variable, nchar(variable) - 1, nchar(variable))]
reglong[, variable := gsub("(BP|CA)$", "", variable)]

reglong[, .N, source]
reglong[, .N, variable]

reglong[, .N, year]
reglong[, uniqueN(Nom), year]
reglong[year == 2015, unique(Nom)]
reglong[year == 2015, paste(unique(Nom), collapse  = "','")]
reglong[year == 2016, paste(unique(Nom), collapse  = "','")]

reg_dict = c('Alsace' = "Grand Est", 
             'Aquitaine' = "Nouvelle-Aquitaine", 
             'Auvergne' = "Auvergne-Rhône-Alpes",
             'Basse-Normandie' = "Normandie",
             'Bourgogne' = "Bourgogne-Franche-Comté", 
             'Bretagne' = 'Bretagne',
             'Centre' = "Centre-Val de Loire",
             'Champagne-Ardenne' = "Grand Est", 
             'Corse' = 'Corse CTU',
             'Corse CTU' = 'Corse CTU',
             'Franche-Comté' = "Bourgogne-Franche-Comté", 
             'Guadeloupe' = 'Guadeloupe',
             'Guyane' = "Guyane CTU",
             'Haute-Normandie' = "Normandie", 
             'Ile-de-France' = 'Ile-de-France',
             'Languedoc-Roussillon' = "Occitanie",
             'Limousin' = "Centre-Val de Loire",
             'Lorraine' = "Grand Est",
             'Martinique' = "Martinique CTU",
             'Midi-Pyrénées' = "Occitanie",
             'Nord-Pas-de-Calais' = "Hauts-de-France", 
             'Pays de la Loire' = 'Pays de la Loire',
             'Picardie' = "Hauts-de-France",
             'Poitou-Charentes' ="Nouvelle-Aquitaine", 
             'Provence-Alpes-Côte d\'Azur' = 'Provence-Alpes-Côte d\'Azur',
             'Rhône-Alpes' = "Auvergne-Rhône-Alpes",
             'Réunion' = 'Réunion'
             )

reglong[, reg16 := ifelse(Nom %in% names(reg_dict), reg_dict[Nom], Nom)]


reglong[, .N, .(Nom, reg16)]

regl = reglong[year >= 2015 & year <= 2024, .(value = sum(value)), 
               by = .(reg16, year, source, variable)]

regl[, .N, reg16]

totl = regl[!(reg16 %in% c("Guadeloupe", "Réunion")), 
            .(value = sum(value)), .(year, variable, source)][, 
            .(value = mean(value)), .(variable, source)]

totw = totl |> dcast(variable ~ source)

totw[c(4, 16, 1, 17, 8, 3, 18, 9)] |> View()
