<?php

defined('BASEPATH') or exit('No direct script access allowed');

class User extends CI_Controller
{
    public function index()
    {
        $this->load->view('templates/logged_user_header_dark');
        $this->load->view('user/index');
        $this->load->view('templates/user_footer');
    }
}
