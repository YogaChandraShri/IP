<?php
session_start();
include 'db_connect.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password']; // No hashing

    // Insert directly into the database
    $stmt = $conn->prepare("INSERT INTO users (UserName, Passwd) VALUES (?, ?)");
    $stmt->bind_param("ss", $username, $password);

    if ($stmt->execute()) {
        header("Location: login.html");
        exit();
    } else {
        echo "Signup failed. Username may already exist.";
    }

    $stmt->close();
}
$conn->close();
?>
