<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IRIS Images</title>
    <link rel="stylesheet" href="./stylesv2.css">
</head>
<body>
    <header class="header">
        <h1>See our Flowers!!!</h1>
    </header>
    <div class="gallery">
        <?php
        $imageDir = 'images/';
        $images = glob($imageDir . "*.{jpg,jpeg,png,gif}", GLOB_BRACE);

        foreach ($images as $index => $image) {
            echo '<img src="' . $image . '" alt="Image ' . ($index + 1) . '">';
        }
        ?>
    </div>
</body>
</html>
