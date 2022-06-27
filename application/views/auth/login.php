<div class="container-fluid mt-5">
	<div class="col-lg-6 offset-lg-3 offset-md-3">
		<div class="p-5">

			<h1 class="text-center mb-5" style="color: #3E6D81; font-size: 50px"><b>Sign In</b></h1>
			<?= $this->session->flashdata('message'); ?>
			<form method="post" action="<?= base_url('auth'); ?>">
				<div class="mb-3">
					<label for="email" class="form-label">Email</label>
					<input type="text" name="email" class="form-control" id="email" placeholder="Input Email" value="<?= set_value('email'); ?>">
					<?= form_error('email', ' <small class="text-danger">', '</small>') ?>
				</div>

				<div class="mb-1">
					<label for="password" class="form-label">Password</label>
					<input type="password" name="password" class="form-control" placeholder="Input Password">
					<?= form_error('password', ' <small class="text-danger">', '</small>') ?>
				</div>

				<div class="mt-2 mb-4">
					<a href="#" style="float:right; color: black; text-decoration: none;">Forgot Password?</a>
				</div>

				<br>

				<div class="d-grid mb-2 mt-2">
					<button type="submit" name="submit" class="btn btn-block text-light" style="background-color: #3E6D81">Login</button>
				</div>
			</form>

			<div class="text-center">
				<p>Don't have an account? <a href="<?= base_url('auth/registration'); ?>" style="color: black; text-decoration: none;"> <b>Sign Up</b> </a></p>
			</div>
		</div>
	</div>
</div>