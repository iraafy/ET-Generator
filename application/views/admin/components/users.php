<h4> <b>Users</b> </h4>

<table class="table table-bordered mt-4">
    <thead>
        <tr>
            <th>NO</th>
            <th>Name</th>
            <th>Email</th>
            <!-- <th>Account Type</th> -->
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
        <?php $no = 1 ?>
        <?php foreach ($users as $list_user) { ?>
            <tr>
                <td>
                    <?= $no; ?>
                </td>
                <td>
                    <?= $list_user['name']; ?>
                </td>
                <td>
                    <?= $list_user['email']; ?>
                </td>
                <td>
                    hapus
                </td>
            </tr>
            <?php $no++ ?>
        <?php } ?>
    </tbody>
</table>