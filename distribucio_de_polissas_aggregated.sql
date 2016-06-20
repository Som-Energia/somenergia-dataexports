(select
    'PROVINCE' AS tipus,
    provincia AS nombre,
    count(provincia)  AS recuento
    FROM
    (
        select   
            provincia.name as provincia,
            comunitat.name AS comunitat_autonoma
            from giscedata_polissa polissa
            left join res_partner rp on rp.id = polissa.soci
            inner join giscedata_cups_ps cups on polissa.cups = cups.id
            left join res_municipi  municipi on cups.id_municipi=municipi.id
            left join res_country_state provincia on provincia.id = municipi.state
            LEFT JOIN res_comunitat_autonoma AS comunitat ON comunitat.id = provincia.comunitat_autonoma
        where polissa.data_alta <= %(date)s and 
               (polissa.data_baixa is null or
              polissa.data_baixa > %(date)s) and
            TRUE
    ) AS taula_provincia
GROUP BY provincia, comunitat_autonoma
ORDER BY comunitat_autonoma, provincia
)
UNION ALL
(
    SELECT
    'STATE' as tipus,
    comunitat_autonoma AS nombre,
    count(comunitat_autonoma) AS recuento
    FROM(
        select   
            provincia.name as provincia,
            comunitat.name AS comunitat_autonoma
            from giscedata_polissa polissa
            left join res_partner rp on rp.id = polissa.soci
            inner join giscedata_cups_ps cups on polissa.cups = cups.id
            left join res_municipi  municipi on cups.id_municipi=municipi.id
            left join res_country_state provincia on provincia.id = municipi.state
            LEFT JOIN res_comunitat_autonoma AS comunitat ON comunitat.id = provincia.comunitat_autonoma
        where polissa.data_alta <= %(date)s and 
               (polissa.data_baixa is null or
              polissa.data_baixa > %(date)s) and
            TRUE

    ) as taula_comunitat_autonoma
    GROUP BY comunitat_autonoma
    ORDER BY taula_comunitat_autonoma.comunitat_autonoma
)
UNION ALL
(
    SELECT
    'COUNTY' as tipus,
    comarca AS nombre,
    count(comarca) AS recuento
    FROM(
        select   
            comarca.name as comarca,
            comunitat.name AS comunitat_autonoma
            from giscedata_polissa polissa
            left join res_partner rp on rp.id = polissa.soci
            inner join giscedata_cups_ps cups on polissa.cups = cups.id
            left join res_municipi municipi on cups.id_municipi=municipi.id
            left join res_comarca comarca on comarca.id = municipi.comarca
            left join res_country_state provincia on provincia.id = municipi.state
            LEFT JOIN res_comunitat_autonoma AS comunitat ON comunitat.id = provincia.comunitat_autonoma
        where polissa.data_alta <= %(date)s and 
               (polissa.data_baixa is null or
              polissa.data_baixa > %(date)s) and
              comunitat.name != 'Cataluña'
    ) as taula_comarca
    WHERE comarca IS NOT NULL
    GROUP BY comarca,comunitat_autonoma
    ORDER BY comunitat_autonoma,comarca)
UNION ALL
(
    SELECT
    'COUNTRY' as tipus,
    pais AS nombre,
    count(pais) AS recuento
    FROM(
        select   
            pais.name as pais
            from giscedata_polissa polissa
            left join res_partner rp on rp.id = polissa.soci
            inner join giscedata_cups_ps cups on polissa.cups = cups.id
            left join res_municipi municipi on cups.id_municipi=municipi.id
            left join res_comarca comarca on comarca.id = municipi.comarca
            left join res_country_state provincia on provincia.id = municipi.state
            LEFT JOIN res_comunitat_autonoma AS comunitat ON comunitat.id = provincia.comunitat_autonoma
            left join res_country as pais on pais.id= provincia.country_id
        where polissa.data_alta <= %(date)s and 
               (polissa.data_baixa is null or
              polissa.data_baixa > %(date)s) and
              pais.name != 'España'
    ) as taula_pais
    GROUP BY pais
    ORDER BY pais
    
)
