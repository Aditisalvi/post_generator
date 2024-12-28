<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cat Animation</title>
  <style>
    body {
      margin: 0;
      overflow: hidden;
      background-color: #f9f9f9;
    }
    .cat {
      position: absolute;
      bottom: 0;
      left: -200px;
      width: 150px;
      height: auto;
    }
  </style>
</head>
<body>
  <img src="https://assets3.lottiefiles.com/private_files/lf30_5ttqPi.json" alt="cat" class="cat" id="cat">

  <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
  <script>
    // Move the cat from left to right in a loop
    anime({
      targets: '#cat',
      translateX: window.innerWidth + 200, // Moves across the screen
      easing: 'linear',
      duration: 8000,
      loop: true
    });
  </script>
</body>
</html>
