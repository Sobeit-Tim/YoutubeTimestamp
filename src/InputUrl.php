<?php
    $url = $_POST["url"];
    
    if ($url == "") {
        echo "<script>alert('Error: There is no input url');</script>";
    } else {
        echo "<script>alert('Input url: {$url}');</script>";
    }

    // echo "<script>alert('Input url: {$url}');</script>";
    
    // $test = "Input url: {$url}";
    // $inputUrl = shell_exec("C:\Users\sukam\AppData\Local\Programs\Python\Python37-32\python.exe server.py" . $test);
?>