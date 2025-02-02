<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize input to prevent XSS
    function cleanInput($data) {
        return htmlspecialchars(strip_tags(trim($data)));
    }

    $name = cleanInput($_POST['name']);
    $email = filter_var(cleanInput($_POST['email']), FILTER_VALIDATE_EMAIL);
    $message = cleanInput($_POST['message']);

    if (!$email) {
        die("Invalid email address.");
    }


    echo "Message sent successfully!";
}
?>
