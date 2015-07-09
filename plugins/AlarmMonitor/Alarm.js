var Jetzt = new Date();
var Start = Jetzt.getTime();

function ZeitAnzeigen () {
  var absSekunden = Math.round(ZeitBerechnen());
  var relSekunden = absSekunden % 60;
  var absMinuten = Math.abs(Math.round((absSekunden - 30) / 60));
  var anzSekunden = "" + ((relSekunden > 9) ? relSekunden : "0" + relSekunden);
  var anzMinuten = "" + ((absMinuten > 9) ? absMinuten : "0" + absMinuten);
document.getElementById('timer').innerHTML = anzMinuten + ":" + anzSekunden;
  window.setTimeout("ZeitAnzeigen()", 1000);
}

function ZeitBerechnen () {
  var Immernoch = new Date();
  return ((Immernoch.getTime() - Start) / 1000);
}
