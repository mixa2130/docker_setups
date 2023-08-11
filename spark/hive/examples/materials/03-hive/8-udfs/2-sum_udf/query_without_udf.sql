use example;

create temporary macro sum_octets(octets array<int>)
cast(octets[0] + octets[1] + octets[2] + octets[3] as int);

create temporary macro octets_to_int(octets array<string>)
array(
	cast(octets[0] as int),
	cast(octets[1] as int),
	cast(octets[2] as int),
	cast(octets[3] as int)
);

select sum_octets(octets_to_int(octets)) result
from (
	select split(ip, '\\.') octets from subnets
) as oct limit 10;
