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
    <nav class="navbar navbar-expand-lg navbar-light ps-3 pe-3 fixed-top" style=" background-color: white !important; box-shadow: 0px 0px 10px -2px rgba(0,0,0,0.35);">
        <div class="container-fluid ">
            <a class="navbar-brand" href="<?= base_url('user'); ?>">
                <img src="<?= base_url('assets/img/'); ?>logo.png" width="60%" alt="">
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0" style="font-weight: 700;">
                    <li class="nav-item">
                        <a class="nav-link" style="color: #3E6D81 !important;" aria-current="page" href="<?= base_url('user') ?>">Home&emsp;</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" style="color: #3E6D81 !important;" aria-current="page" href="<?= base_url('user/demo') ?>">Demo&emsp;</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" style="color: #3E6D81 !important;" aria-current="page" href="<?= base_url('user/userguide') ?>">User Guide&emsp;</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link btn btn-sm text-center ps-4 pe-4 pt-1 pb-1 mt-1" style="background-color: #3E6D81; text-align: center; border-radius: 40px; color: white !important;" aria-current="page" href="<?= base_url('auth') ?>"><b>Sign In</b></a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>