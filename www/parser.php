<?php
//Data from TRBOS-FMS http://www.lfs-bw.de/Fachthemen/Digitalfunk-Funk/Documents/Pruefstelle/TRBOS-FMS.pdf


	function parse($mode, $fms)
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

		switch ($mode) {
			case "service":
				return $service[substr($fms,0,1)];
				break;
				
			case "country":
				return $country[substr($fms,1,1)];
				break;
				
			case "direction":
				if(substr($fms,9,1) == 1){
					return "L->F";
				}elseif(substr($fms,9,1) == 0){
					return "F->L";
				}
				break;

			default:
				return "Parser: mode error!";
		}
	}

?>