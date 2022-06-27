<?php

defined('BASEPATH') or exit('No direct script access allowed');

class Generate extends CI_Controller
{
    public function index()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('generate/index');
    }

    public function question_collection()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('generate/question_collection');
    }

    public function generate_question()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('user/generate');
    }
}
