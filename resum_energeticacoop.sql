select
	p.name as n_contrato_SomEnergia,
	p.state,
	p.data_firma_contracte as fecha_solicitud,
	p.data_alta as alta_contrato,
	p.data_baixa as baja_contrato,
	p.potencia,
	p.data_ultima_lectura as ultima_lectura_facturada,
	titular.name as titular,
	cups.name as CUPS, 
	cups.direccio as direccion,
	cnae.name as CNAE,
	cnae.descripcio as CNAE_descripcion,
	case when check_soci.category_id='8'
		then 'Titular Soci Som Energia'
		else 'Titular NO Soci Som Energia'
		end as Soci_de_Som,
	case when p.donatiu=false
		then 'No'
		else 'Si'
		end as donativo_voluntario, 
	cups.conany_kwh as Consumo_anual_estimado,
	cups.conany_origen as Metodo_calculo_consumo_anual,
	cups.conany_data as fecha_calculo_consumo_anual

	

from giscedata_polissa as p
left join giscedata_cups_ps as cups on cups.id=p.cups
left join giscemisc_cnae as cnae on cnae.id=p.cnae
left join res_partner as titular on p.titular=titular.id
left join res_partner_category_rel as check_soci on (check_soci.partner_id=titular.id and check_soci.category_id='8')
where p.soci=38039 --Energetica
order by
p.name
