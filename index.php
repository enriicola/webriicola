<?php
/**
 * Dynamic Homepage for Webriicola
 * Automatically lists all sub-folders containing an index.html
 */

function get_project_title($path) {
    $index_content = @file_get_contents($path . '/index.html');
    if ($index_content && preg_match('/<title>(.*?)<\/title>/is', $index_content, $matches)) {
        return trim($matches[1]);
    }
    return ucfirst(basename($path));
}

$projects = [];
$dirs = array_filter(glob('*'), 'is_dir');

foreach ($dirs as $dir) {
    if (file_exists($dir . '/index.html')) {
        $projects[] = [
            'name' => get_project_title($dir),
            'path' => $dir
        ];
    }
}

// Sort alphabetically
usort($projects, function($a, $b) {
    return strcasecmp($a['name'], $b['name']);
});
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>webriicola</title>
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <img src="ricola.jpg" alt="Ricola" class="hero-img">
            <h1>web + enriicola = webriicola</h1>
            <p class="subtitle">My personal website! A collection of mini webapps</p>
        </header>

        <script src="https://keepandroidopen.org/banner.js"></script>

        <main class="grid">
            <?php foreach ($projects as $project): ?>
                <a href="<?= htmlspecialchars($project['path']) ?>/" class="card">
                    <div class="card-content">
                        <h2><?= htmlspecialchars($project['name']) ?></h2>
                    </div>
                </a>
            <?php endforeach; ?>
            
            <?php if (empty($projects)): ?>
                <p>No projects found.</p>
            <?php endif; ?>
        </main>
    </div>
</body>
</html>
