<?php
session_start();

// Generate CSRF token
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>CSRF Demo</title>
</head>
<body>

<h2>Vulnerable Form</h2>
<form method="POST">
    <input type="email" name="email_bad" placeholder="Enter email">
    <button type="submit" name="update_bad">Update</button>
</form>

<?php
if (isset($_POST['update_bad'])) {
    // VULNERABLE: No CSRF protection
    echo "Updated email to: " . $_POST['email_bad'];
}
?>

<hr>

<h2>Secure Form (CSRF Protection)</h2>
<form method="POST">
    <input type="email" name="email_good" placeholder="Enter email">
    <input type="hidden" name="csrf_token" value="<?php echo $_SESSION['csrf_token']; ?>">
    <button type="submit" name="update_good">Update</button>
</form>

<?php
if (isset($_POST['update_good'])) {

    // Verify CSRF token
    if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
        die("CSRF validation failed");
    }

    // SECURE output handling too
    $email = htmlspecialchars($_POST['email_good'], ENT_QUOTES, 'UTF-8');

    echo "Safely updated email to: " . $email;
}
?>

</body>
</html>