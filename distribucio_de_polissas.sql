select  pais.code as codi_pais,
	pais.name as pais, 
	comunitat.codi as codi_ccaa, 
	comunitat.name as comunitat_autonoma, 
	provincia.code as codi_provincia, 
	provincia.name as provincia, 
	municipi.ine as codi_ine, 
    municipi.name as municipi, 
	count(polissa.id) as quants 
	from giscedata_polissa polissa
	left join res_partner rp on rp.id = polissa.soci
	inner join giscedata_cups_ps cups on polissa.cups = cups.id
	left join res_municipi  municipi on cups.id_municipi=municipi.id
	left join res_country_state provincia on provincia.id = municipi.state
	LEFT JOIN res_comunitat_autonoma AS comunitat ON comunitat.id = provincia.comunitat_autonoma
	left join res_country as pais on pais.id = provincia.country_id
where (polissa.data_baixa >= %(date)s 
        or polissa.data_baixa is null) and 
    polissa.data_alta <= %(date_end)s and
	TRUE
GROUP BY
	codi_pais,
	codi_ccaa,
	codi_provincia,
	codi_ine,
	pais,
	provincia,
	municipi,
	comunitat.name
ORDER BY
	pais ASC,
	comunitat_autonoma ASC,
	provincia ASC,
	municipi ASC,
	TRUE ASC
