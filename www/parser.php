<?php
//Data from TRBOS-FMS http://www.lfs-bw.de/Fachthemen/Digitalfunk-Funk/Documents/Pruefstelle/TRBOS-FMS.pdf

	function parse($mode, $data)
	{	
		//Data for Service Parsing
		
		$service = array(
		"0" => "Unbekannt",
		"1" => "Polizei",
		"2" => "Bundesgrenzschutz",
		"3" => "Bundeskriminalamt",
		"4" => "Katastrophenschutz",
		"5" => "Zoll",
		"6" => "Feuerwehr",
		"7" => "Technisches Hilfswerk",
		"8" => "Arbeiter-Samariter-Bund",
		"9" => "Deutsches Rotes Kreuz",
		"a" => "Johanniter-Unfall-Hilfe",
		"b" => "Malteser-Hilfsdienst",
		"c" => "Deutsche Lebensrettungsgesellschaft",
		"d" => "Rettungsdienst",
		"e" => "Zivilschutz",
		"f" => "Fernwirktelegramm",
	);

	//Data for Country Parsing
	$country = array(
		"0" => "Sachsen",
		"1" => "Bund",
		"2" => "Baden-Württemberg",
		"3" => "Bayern I",
		"4" => "Berlin",
		"5" => "Bremen",
		"6" => "Hamburg",
		"7" => "Hessen",
		"8" => "Niedersachsen",
		"9" => "Nordrhein-Westfalen",
		"a" => "Rheinland-Pflaz",
		"b" => "Schleswig-Holstein",
		"c" => "Saarland",
		"d" => "Bayern II",
		"e" => "Meck-Pom/Sachsen-Anhalt",
		"f" => "Brandenburg/Thüringen",
	);
	
	//Data for Location Parsing
	$location = array(
		"11" => "testLoc",
		"22" => "testLoc",
		"33" => "testLoc"
	);
	
	//Data for Vehicle Parsing
	$vehicle = array(
		"1111" => "testVeh",
		"2222" => "testVeh",
		"3333" => "testVeh"
	);
	
	
	//Data for ZVEI Parsing
	$country = array(
		"12345" => "testZvei",
		"23456" => "testZvei",
		"34567" => "testZvei",
	);

	
		switch ($mode) {
			//Parse Service
			case "service":
				if (array_key_exists($data, $service))
				{
					return $service[substr($data,0,1)];
				}else
				{
					return $data;
				}
				break;
			
			//Parse Country
			case "country":
				if (array_key_exists($data, $country))
				{
					return $country[substr($data,1,1)];
				}else
				{
					return $data;
				}
				break;
				
			//Parse Location
			case "location":
				if (array_key_exists($data, $location))
				{
					return $location[substr($data,2,2)];
				}else
				{
					return $data;
				}
				break;
				
			//Parse Vehicle
			case "vehicle":
				if (array_key_exists($data, $vehicle))
				{
					return $vehicle[substr($data,4,4)];
				}else
				{
					return $data;
				}
				break;
			
			//Parse direction
			case "direction":
				if(substr($fms,9,1) == 1
				{
					return "L->F";
				}elseif(substr($fms,9,1) == 0
				{
					return "F->L";
				}else
					return "ERR!";
				}
				break;
	
			//Parse Zvei
			case "zvei":
				if (array_key_exists($data, $zvei))
				{
					return $data ." - ". $zvei[$data];
				}else
				{
					return $data;
				}
				break;

			default:
				return "Parser: mode error!";
		}
	}

?>