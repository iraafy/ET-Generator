<?php

defined('BASEPATH') or exit('No direct script access allowed');

class CBT extends CI_Controller
{
    public function index()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('CBT/index');
        $this->load->view('templates/auth_footer');
    }

    public function start_test()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('CBT/start_test');
        $this->load->view('templates/auth_footer');
    }

    public function result_test()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('templates/auth_footer');
    }
}
