<?php

$db = new SQLite3('test.db');

$db->exec("CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)");

$db->exec("INSERT INTO users (username, password)
           SELECT 'admin', '1234'
           WHERE NOT EXISTS (
               SELECT 1 FROM users WHERE username='admin'
           )");

?>

<!DOCTYPE html>
<html>
<head>
    <title>SQL Injection Demo (SQLite)</title>
</head>
<body>

<h2>Vulnerable Login</h2>
<form method="POST">
    <input type="text" name="username" placeholder="Username">
    <input type="text" name="password" placeholder="Password">
    <button type="submit" name="login_bad">Login</button>
</form>

<?php
if (isset($_POST['login_bad'])) {

    $u = $_POST['username'];
    $p = $_POST['password'];

    // VULNERABLE
    $sql = "SELECT * FROM users WHERE username='$u' AND password='$p'";
    $result = $db->query($sql);

    $row = $result->fetchArray();

    echo ($row) ? "Login Success (Vulnerable)" : "Login Failed";
}
?>

<hr>

<h2>Secure Login (Prepared Statement)</h2>
<form method="POST">
    <input type="text" name="username_safe" placeholder="Username">
    <input type="text" name="password_safe" placeholder="Password">
    <button type="submit" name="login_good">Login</button>
</form>

<?php
if (isset($_POST['login_good'])) {

     # Secure: Use prepared statements to prevent SQL injection
    $stmt = $db->prepare("SELECT * FROM users WHERE username = :username AND password = :password");
    $stmt->bindValue(':username', $_POST['username_safe'], SQLITE3_TEXT);
    $stmt->bindValue(':password', $_POST['password_safe'], SQLITE3_TEXT);

    $result = $stmt->execute();
    $row = $result->fetchArray();

    echo ($row) ? "Login Success (Secure)" : "Login Failed";
}
?>

</body>
</html>