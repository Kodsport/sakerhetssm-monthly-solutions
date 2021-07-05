<?php

if (isset($_GET['cmd'])) {
    if (preg_match('/[0123456789!"#$%&\\\\\'()*+,\\-:<=>?@[\\\\\\]^_{|}~]/', $_GET['cmd']) === 0) {
        eval($_GET['cmd']);
    } else {
        echo 'ajabaja';
    }
}

highlight_file(__FILE__);
