(
SELECT
    'PROVINCE' AS tipus,
    provincia AS nombre,
    count(provincia)  AS recuento
FROM(
	SELECT
        adreces.id, 
		adreces.partner_id, 
		municipi.name AS municipi, 
		comarca.name AS comarca,
		provincia.name AS provincia,
		comunitat.name AS comunitat_autonoma,
		pais.name AS pais
		
	FROM
        res_partner_address AS adreces
	LEFT JOIN (
		SELECT
            dades_inicials.partner_id,
            MIN(dades_inicials.id) AS id_unic
		FROM
            res_partner_address as dades_inicials
		WHERE
            dades_inicials.active
		GROUP BY dades_inicials.partner_id
		) as dades_inicials ON dades_inicials.id_unic = adreces.id
	LEFT JOIN res_partner_category_rel AS category
        ON category.partner_id = dades_inicials.partner_id
	LEFT JOIN res_municipi AS municipi
        ON municipi.id = adreces.id_municipi
	LEFT JOIN res_comarca AS comarca
        ON comarca.id = municipi.comarca
	LEFT JOIN res_country_state AS provincia
        ON provincia.id = adreces.state_id
	LEFT JOIN res_comunitat_autonoma AS comunitat
        ON comunitat.id = provincia.comunitat_autonoma
	LEFT JOIN res_country AS pais
        ON pais.id = adreces.country_id

	WHERE adreces.partner_id IS NOT NULL
		AND category.category_id = 8
		AND adreces.create_date < '2015-09-01'
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
	SELECT
        adreces.id, 
		adreces.partner_id, 
		municipi.name AS municipi, 
		comarca.name AS comarca,
		provincia.name AS provincia,
		comunitat.name AS comunitat_autonoma,
		pais.name AS pais
		
	FROM res_partner_address AS adreces
	LEFT JOIN (
		SELECT dades_inicials.partner_id, MIN(dades_inicials.id) AS id_unic
		FROM res_partner_address as dades_inicials
		WHERE dades_inicials.active
		group by dades_inicials.partner_id
		) AS dades_inicials
        ON dades_inicials.id_unic = adreces.id
	LEFT JOIN res_partner_category_rel AS category
        ON category.partner_id = dades_inicials.partner_id
	LEFT JOIN res_municipi AS municipi
        ON municipi.id = adreces.id_municipi
	LEFT JOIN res_comarca AS comarca
        ON comarca.id = municipi.comarca
	LEFT JOIN res_country_state AS provincia ON provincia.id = adreces.state_id
	LEFT JOIN res_comunitat_autonoma AS comunitat ON comunitat.id = provincia.comunitat_autonoma
	LEFT JOIN res_country AS pais ON pais.id = adreces.country_id

	WHERE adreces.partner_id IS NOT NULL
		AND category.category_id = 8
		AND adreces.create_date < '2015-09-01') as taula_comunitat_autonoma
GROUP BY comunitat_autonoma
ORDER BY taula_comunitat_autonoma.comunitat_autonoma)

UNION ALL

(
SELECT
    'COUNTY' as tipus,
    comarca AS nombre,
    count(comarca) AS recuento
FROM(
	SELECT adreces.id, 
		adreces.partner_id, 
		municipi.name AS municipi, 
		comarca.name AS comarca,
		provincia.name AS provincia,
		comunitat.name AS comunitat_autonoma,
		pais.name AS pais
		
	FROM res_partner_address AS adreces
	LEFT JOIN (
		SELECT dades_inicials.partner_id, MIN(dades_inicials.id) AS id_unic
		FROM res_partner_address as dades_inicials
		WHERE dades_inicials.active
		group by dades_inicials.partner_id
		) as dades_inicials ON dades_inicials.id_unic = adreces.id
	LEFT JOIN res_partner_category_rel AS category ON category.partner_id = dades_inicials.partner_id
	LEFT JOIN res_municipi AS municipi ON municipi.id = adreces.id_municipi
	LEFT JOIN res_comarca AS comarca ON comarca.id = municipi.comarca
	LEFT JOIN res_country_state AS provincia ON provincia.id = adreces.state_id
	LEFT JOIN res_comunitat_autonoma AS comunitat ON comunitat.id = provincia.comunitat_autonoma
	LEFT JOIN res_country AS pais ON pais.id = adreces.country_id

	WHERE adreces.partner_id IS NOT NULL
		AND category.category_id = 8
		AND adreces.create_date < '2015-09-01'
		AND comunitat.name != 'Cataluña') as taula_comarca
WHERE comarca IS NOT NULL
GROUP BY comarca, comunitat_autonoma
ORDER BY comunitat_autonoma, comarca)

UNION ALL

(
SELECT
    'COUNTRY' as tipus,
    pais AS nombre,
    count(pais) AS recuento
FROM(
	SELECT adreces.id, 
		adreces.partner_id, 
		municipi.name AS municipi, 
		comarca.name AS comarca,
		provincia.name AS provincia,
		comunitat.name AS comunitat_autonoma,
		pais.name AS pais
		
	FROM res_partner_address AS adreces
	LEFT JOIN (
		SELECT dades_inicials.partner_id, MIN(dades_inicials.id) AS id_unic
		FROM res_partner_address as dades_inicials
		WHERE dades_inicials.active
		group by dades_inicials.partner_id
		) as dades_inicials ON dades_inicials.id_unic = adreces.id
	LEFT JOIN res_partner_category_rel AS category ON category.partner_id = dades_inicials.partner_id
	LEFT JOIN res_municipi AS municipi ON municipi.id = adreces.id_municipi
	LEFT JOIN res_comarca AS comarca ON comarca.id = municipi.comarca
	LEFT JOIN res_country_state AS provincia ON provincia.id = adreces.state_id
	LEFT JOIN res_comunitat_autonoma AS comunitat ON comunitat.id = provincia.comunitat_autonoma
	LEFT JOIN res_country AS pais ON pais.id = adreces.country_id

	WHERE adreces.partner_id IS NOT NULL
		AND category.category_id = 8
		AND adreces.create_date < '2015-09-01'
		AND pais.name != 'España'
		) as taula_pais
GROUP BY pais
ORDER BY pais)
