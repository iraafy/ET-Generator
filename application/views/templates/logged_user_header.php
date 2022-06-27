<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <script src="https://code.iconify.design/2/2.1.2/iconify.min.js"></script>
    <title><?= $title; ?></title>
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-light ps-3 pe-3 fixed-top" style=" background-color: #3E6D81 !important; box-shadow: 0px 0px 10px -2px rgba(0,0,0,0.35);">
        <div class="container-fluid ">
            <a class="navbar-brand" href="#">
                <img src="<?= base_url('assets/img/'); ?>logo-light.png" width="60%" alt="">
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0" style="font-weight: 600;">
                    <li class="nav-item">
                        <a class="nav-link" style="color: white !important;" aria-current="page" href="<?= base_url('user') ?>">Home&emsp;</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" style="color: white !important;" aria-current="page" href="<?= base_url('user/question_collection') ?>">Question Collection&emsp;</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" style="color: white !important;" aria-current="page" href="<?= base_url('user/generate') ?>">Generate&emsp;</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" style="color: white !important;" aria-current="page" href="<?= base_url('user/cbt') ?>">CBT&emsp;</a>
                    </li>
                    <li class="nav-item p-0">
                        <div class="dropdown">
                            <button class="btn dropdown-toggle" style="color: white;" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                                <span class="iconify" style="font-size: 25px; color: white" data-icon="healthicons:ui-user-profile-outline"></span>
                            </button>
                            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                                <a class="dropdown-item" href="#">
                                    <?php
                                    if (!isset($_SESSION["login"])) {
                                        echo "Profil";
                                    } else {
                                        echo $_SESSION["username"];
                                    }
                                    ?>
                                </a>
                                <?php
                                if (isset($_SESSION["login"])) {
                                    echo
                                    "
										<a class='dropdown-item' href='logout.php'>
											<span class='iconify-inline' data-icon='carbon:logout'></span>
										</a>
										";
                                } else {
                                    echo
                                    "
										<a class='dropdown-item' href='login.php'>
											Masuk
										</a>
										";
                                }
                                ?>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </nav>