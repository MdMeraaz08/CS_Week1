<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars($_POST['name']);
    $email = htmlspecialchars($_POST['email']);
    $message = htmlspecialchars($_POST['message']);
    echo "<h2>Thank You, $name</h2>";
    echo "<p>We have received your message.</p>";
}
?>