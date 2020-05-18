<?php
    $url = $_POST["url"];
    // echo "<script>alert('Input url: {$url}');</script>";
    
    $test = "Input url: {$url}";
    $inputUrl = shell_exec("C:\Users\sukam\AppData\Local\Programs\Python\Python37-32\python.exe server.py" . $test);
?>