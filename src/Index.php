<?php
  $conn = mysqli_connect("localhost", "root", "1111", "ytg");

  mysqli_query($conn, "set session character_set_connection=utf8");
  mysqli_query($conn, "set session character_set_results=utf8");
  mysqli_query($conn, "set session character_set_client=utf8");

  $sql = "select score from comment";
  $result = mysqli_query($conn, $sql);
  $num = mysqli_num_rows($result);
  $sum = 0;
  
  for ($i = 1; $i <= $num; $i++) {
    $row = mysqli_fetch_array($result);
    $score = $row["score"];
    $sum += $score;
  }
  
  if ($num == 0) {
    $avg = 0;
  } else {
    $avg = $sum / $num;
  }
?>

<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>YouTube Timestamp Generator</title>
</head>
<body>
  <h2>YouTube Timestamp Generator</h2><br><br>
  Welcome to the YouTube Timestamp Generator web page!<br>
  This page is for prototype about feature to sign up your score and make some comments.<br><br>
  <form action="Comment.php" method="post">
    Score
    <select name="score">
      <option value="NULL">Select your score</option>
      <option value="5">5</option>
      <option value="4.5">4.5</option>
      <option value="4">4</option>
      <option value="3.5">3.5</option>
      <option value="3">3</option>
      <option value="2.5">2.5</option>
      <option value="2">2</option>
      <option value="1.5">1.5</option>
      <option value="1">1</option>
      <option value="0.5">0.5</option>
      <option value="0">0</option>
    </select><br><br>
    Comment<br>
    <input type="text" name="text" style="width:400px;height:100px;"><br><br>
    <input type="submit" value="Submit">
  </form><br>
  Average:
  <?php
    echo round($avg, 2);
    echo "<br><br>";
    echo "Score&nbsp&nbsp&nbsp&nbsp&nbspComment<br>";
    $sql = "select * from comment";
    $result = mysqli_query($conn, $sql);
    for ($i = 1; $i <= $num; $i++) {
      $row = mysqli_fetch_array($result);
      $score = $row["score"];
      $text = $row["text"];
      echo "{$score}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{$text}<br>";
    }
    echo "<br>";
  ?>
</body>
</html>