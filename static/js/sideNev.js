function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

$(function () {
  count = 0;
  wordsArray = [
  "Bonjour", "Guten Tag",
   "Hola", "Salve",
   "Yassas", "Zdravstvuyte",
   "Konnichiwa", "Olá",
   "Goddag", "Goedendag",
   "Shikamoo", "Dzień dobry",
   "Namaskar", "Merhaba"
  ];
  setInterval(function () {
    count++;
    $("#word").fadeOut(400, function () {
      $(this).text(wordsArray[count % wordsArray.length]).fadeIn(400);
    });
  }, 2000);
});