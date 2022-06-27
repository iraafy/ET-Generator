<div class="container-fluid mt-5">
    <div class="col-lg-6 offset-lg-3 offset-md-3">
        <div class="p-5">

            <h1 class="text-center mb-5" style="color: #3E6D81; font-size: 50px"><b>Sign Up</b></h1>
            <form method="post" action="<?= base_url('auth/registration'); ?>">
                <div class="mb-3">
                    <label for="name" class="form-label">Name</label>
                    <input type="text" name="name" class="form-control" id="name" placeholder="Input Name" value="<?= set_value('name'); ?>">
                    <?= form_error('name', ' <small class="text-danger">', '</small>') ?>

                </div>

                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="text" name="email" class="form-control" id="email" placeholder="Input Email" value="<?= set_value('email'); ?>">
                    <?= form_error('email', ' <small class="text-danger">', '</small>') ?>
                </div>

                <div class="mb-4">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" name="password" class="form-control" placeholder="Input Password">
                    <?= form_error('password', ' <small class="text-danger">', '</small>') ?>
                </div>

                <div class="d-grid mb-2 mt-3">
                    <button type="submit" name="register" class="btn btn-block text-light" style="background-color: #3E6D81">Register</button>
                </div>
            </form>

            <div class="text-center">
                <p>Already have an account? <a href="<?= base_url('auth'); ?>" style="color: black; text-decoration: none;"> <b>Sign In</b> </a></p>
            </div>
        </div>
    </div>
</div>