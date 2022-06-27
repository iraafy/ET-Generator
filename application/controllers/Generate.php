<?php

defined('BASEPATH') or exit('No direct script access allowed');

class Generate extends CI_Controller
{
    public function index()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('generate/index');
        $this->load->view('templates/auth_footer');
    }

    public function question_collection()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('generate/question_collection');
    }

    public function generate_error_identification()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('generate/generate_question');
    }

    public function generate_sentence_completion()
    {
        $this->load->view('templates/logged_user_header_light');
    }

    public function generate_vocabulary()
    {
        $this->load->view('templates/logged_user_header_light');
    }

    public function generate_5w1h()
    {
        $this->load->view('templates/logged_user_header_light');
    }

    public function generate_pronoun_reference()
    {
        $this->load->view('templates/logged_user_header_light');
    }

    public function generate_summary()
    {
        $this->load->view('templates/logged_user_header_light');
    }

    public function preview_passage()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('generate/preview_passage');
    }

    public function generate_result()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('generate/generate_result');
        $this->load->view('templates/auth_footer');
    }

    public function add_question()
    {
        $this->load->view('templates/logged_user_header_light');
        $this->load->view('generate/add_question');
        $this->load->view('templates/auth_footer');
    }
}
