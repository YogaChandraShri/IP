<?php
session_start();
include 'db_connect.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password']; // No hashing

    $stmt = $conn->prepare("SELECT * FROM users WHERE UserName=? AND Passwd=?");
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();

    $result = $stmt->get_result();

    if ($result->num_rows == 1) {
        $user = $result->fetch_assoc();
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['username'] = $user['UserName'];

        // Redirect to Flask with username
        header("Location: http://127.0.0.1:5000/home/" . urlencode($user['UserName']));
        exit();
    } else {
        echo "Invalid username or password.";
    }

    $stmt->close();
}
$conn->close();
?>
