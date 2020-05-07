<?php
    $conn = mysqli_connect("localhost", "root", "1111", "ytg");
    
    $score = $_POST["score"];
    $text = $_POST["text"];

    mysqli_query($conn, "set session character_set_connection=utf8");
    mysqli_query($conn, "set session character_set_results=utf8");
    mysqli_query($conn, "set session character_set_client=utf8");

    // remove blank from the text
    $trimmedText = trim($text);
    $trimmedText = preg_replace("/\s+/", "", $trimmedText);
    
    if ($score == "NULL" or $trimmedText == "") {
        echo "<script>alert('You must leave your score and comment.');</script>";
        echo "<meta http-equiv='refresh' content='0;url=Index.php'>";
    } else {
        $sql = "insert into comment values (NULL, '{$score}', '{$text}')";
        mysqli_query($conn, $sql);

        echo "<script>alert('Your comment has successfully signed up.');</script>";
        echo "<meta http-equiv='refresh' content='0;url=Index.php'>";
    }
?>