function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

$(function () {
  count = 0;
  words = [
  "Hello", "Hola",
  "नमस्कार", "Bonjour",
  "નમસ્તે",
  "你好", "Привет",
  "selamat siang", "হ্যালো",
  "Olá", "Halo",
  "Olá", "Guten Tag",
  "こんにちは", "Merhaba",
  "Hujambo", "dzień dobry",
  ];
  words2 = ["ہیلو","مرحبا"];
  wordsArray = words.concat(words2);
  setInterval(function () {
    count++;
    $("#word").fadeOut(400, function () {
      $(this).text(wordsArray[count % wordsArray.length]).fadeIn(400);
    });
  }, 2000);
});