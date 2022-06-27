<?php

defined('BASEPATH') or exit('No direct script access allowed');

class User extends CI_Controller
{
    public function index()
    {
        $this->load->view('templates/logged_user_header');
        $this->load->view('user/index');
        $this->load->view('templates/logged_user_footer');
    }

    public function question_collection()
    {
        $this->load->view('templates/logged_user_header');
        $this->load->view('user/question_collection');
    }

    public function generate()
    {
        $this->load->view('templates/logged_user_header');
        $this->load->view('user/generate');
    }
}
