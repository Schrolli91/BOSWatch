<?php
// TRBOS-FMS  http://www.lfs-bw.de/Fachthemen/Digitalfunk-Funk/Documents/Pruefstelle/TRBOS-FMS.pdf
// FMS Bayern https://www.stmi.bayern.de/assets/stmi/sus/feuerwehr/id2_17a_03_02_fms_kenng_fw_anl1_20020523.pdf

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
		"2" => "Baden-W�rttemberg",
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
		"f" => "Brandenburg/Th�ringen",
	);


	//Data for ZVEI Parsing
	$zvei = array(
		"12345" => "testZvei",
		"23456" => "testZvei",
		"34567" => "testZvei",
	);

	
		switch ($mode) {
			//Parse Service
			case "service":
				$data = substr($data,0,1);
				if (array_key_exists($data, $service))
				{
					return $service[$data];
				}else
				{
					return $data;
				}
				break;
			
			//Parse Country
			case "country":
				$data = substr($data,1,1);
				if (array_key_exists($data, $country))
				{
					return $country[$data];
				}else
				{
					return $data;
				}
				break;	
			
			//Parse direction
			case "direction":
				if (substr($data,9,1) == 1)
				{
					return "L->F";
				}elseif (substr($data,9,1) == 0)
				{
					return "F->L";
				}else
				{
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