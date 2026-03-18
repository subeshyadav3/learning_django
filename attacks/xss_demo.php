<?php

?>

<!DOCTYPE html>
<html>
<head>
    <title>XSS Demo</title>
</head>
<body>

<h2>Vulnerable Version</h2>
<form method="GET">
    <input type="text" name="name" placeholder="Enter your name">
    <button type="submit">Submit</button>
</form>

<?php
if (isset($_GET['name'])) {
    // VULNERABLE: Direct output
    echo "<p>Hello " . $_GET['name'] . "</p>";
}
?>

<hr>

<h2>Secure Version</h2>
<form method="GET">
    <input type="text" name="safe_name" placeholder="Enter your name safely">
    <button type="submit">Submit</button>
</form>

<?php
if (isset($_GET['safe_name'])) {
    // SECURE: Escape output
    $safe = htmlspecialchars($_GET['safe_name'], ENT_QUOTES, 'UTF-8');
    echo "<p>Hello " . $safe . "</p>";
}
?>

</body>
</html>