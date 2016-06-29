select res_partner.name,lang,email 
from res_partner 
left join res_partner_address as address on address.partner_id = res_partner.id 
where res_partner.id in 
	(select titular AS ID from giscedata_polissa  
		left join somenergia_soci on somenergia_soci.partner_id = giscedata_polissa.titular 
	 where active is true and somenergia_soci.partner_id is null 
	 UNION 
	 select pagador AS ID from giscedata_polissa  left join somenergia_soci on somenergia_soci.partner_id = giscedata_polissa.titular 
	 where active is true and somenergia_soci.partner_id is null
	) and address.email is not null and address.active and address.email != ''