<?php

define("dbserver", "127.0.0.1");
define("dbport", 3306);
define("dbusr", "root");
define("dbpass", "wuhonglv");
define("dbname", "pic");


function image_base64($image_binary){
    $base64_image_content = "data:image/png;base64," . chunk_split(base64_encode($image_binary));
    return $base64_image_content;
}


function get_raw_pic($pic_id){
    $dbserver = constant("dbserver");
    $dbusr = constant("dbusr");
    $dbname = constant("dbname");
    $dbpass = constant("dbpass");
    $dbport = constant("dbport");
    $con = mysqli_connect($dbserver, $dbusr, $dbpass, $dbname, $dbport);
    if (!$con)
    {
        die('Could not connect: ' . mysql_error());
    }

    $result = mysqli_query($con, "SELECT `pic` FROM `pic_store` WHERE id=$pic_id");
    echo "<hr>下面这个图片是没有经过图片处理的原始图片，用于参照<br>";
    echo "<img src=\"";
    foreach($result as $k=>$v){
        foreach($v as $vk=>$vv){
            $pic = $vv;
        }
        
    }
    echo image_base64($pic);
    echo "\" height=\"400\" width=\"400\" />";

    mysqli_close($con);

}

function get_changed_pic($pic_id){
    $dbserver = constant("dbserver");
    $dbusr = constant("dbusr");
    $dbname = constant("dbname");
    $dbpass = constant("dbpass");
    $dbport = constant("dbport");
    $con = mysqli_connect($dbserver, $dbusr, $dbpass, $dbname, $dbport);
    if (!$con)
    {
        die('Could not connect: ' . mysql_error());
    }
    $result = mysqli_query($con, "SELECT `uuid`,`group_uuid`,`pic` FROM `pic_store` WHERE id=$pic_id");
    
    echo "<img src=\"";

    
    foreach($result as $k=>$v){
        foreach($v as $vk=>$vv){
            if ($vk=="uuid"){
                $uuid = $vv;
            }
            if ($vk=="group_uuid"){
                $group_uuid = $vv;
            }
            $pic = $vv;
        }
        
    }
    echo image_base64($pic);
    echo "\" height=\"400\" width=\"400\" />";



    mysqli_close($con);

    echo "
    <br>
    <input type=hidden name=group_uuid value='$group_uuid'>
    <input type='radio' name='score_$uuid' value='1'>1
    <input type='radio' name='score_$uuid' value='2'>2
    <input type='radio' name='score_$uuid' value='3'>3
    <input type='radio' name='score_$uuid' value='4'>4
    <input type='radio' name='score_$uuid' value='5'>5
    <input type='radio' name='score_$uuid' value='6'>6
    <input type='radio' name='score_$uuid' value='7'>7
    <input type='radio' name='score_$uuid' value='8'>8
    <input type='radio' name='score_$uuid' value='9'>9
    <input type='radio' name='score_$uuid' value='10'>10";
}


function print_auditor_form(){
    echo '
    <form action="" method="post">
    审计员:
    <input type="input" name="auditor_name" value="">
    ';
}





function print_pic_form($session_views)
{
    if ($session_views == 0){
        print_auditor_form();
    }else{
        echo '
            <form action="" method="post">
    ';
    }

    $dbserver = constant("dbserver");
    $dbusr = constant("dbusr");
    $dbname = constant("dbname");
    $dbpass = constant("dbpass");
    $dbport = constant("dbport");
    $con = mysqli_connect($dbserver, $dbusr, $dbpass, $dbname, $dbport);
    
    $result = mysqli_query($con, "select group_concat(`id`),`group_uuid` from  pic_store group by group_uuid ;");


    foreach($result as $k=>$v){

        // 默认每个人会挑选一组，组别不重复
        if (!in_array($v["group_uuid"], $_SESSION['queried_group_uuid'])){
            array_unshift($_SESSION['queried_group_uuid'], $v["group_uuid"]);
            
            $group_id = $v["group_uuid"];

            $res_group_id = mysqli_query($con, "select `id` from `pic_store` where `group_uuid`='$group_id' and `flag_raw`=1;");
            foreach ($res_group_id as $res_group_id_k => $res_group_id_v) {
                get_raw_pic($res_group_id_v["id"]);
            }

            $pic_id_array = explode(',',$v["group_concat(`id`)"]);

            // echo "<br>";
            // var_dump($pic_id_array);
            // echo "<br>";
            // var_dump(array_rand($pic_id_array, 2));

            echo "<hr>";

            $keys = array_rand($pic_id_array, 2);
            foreach ($keys as $k => $v) {
                get_changed_pic($pic_id_array[$v]);
                echo "<br>";
            }

            echo "<br> <input type='submit' value='查看下一张图片'/></form>";
            break;
        }
    }

    // $_SESSION['queried_group_uuid']


}


function get_pic_score(){
    $dbserver = constant("dbserver");
    $dbusr = constant("dbusr");
    $dbname = constant("dbname");
    $dbpass = constant("dbpass");
    $dbport = constant("dbport");
    $con = mysqli_connect($dbserver, $dbusr, $dbpass, $dbname, $dbport);
    if (!$con)
    {
        die('Could not connect: ' . mysql_error());
    }
    // $result = mysqli_query($con, "SELECT `pic` FROM `pic_store` WHERE id=$pic_id");

    // insert into `pic`.`pic_score` (`group_uuid`, `uuid`, `auditor_name`, `score`) values ('1', '2', '3', '4');
    // $result = mysqli_query($con, "insert into `pic`.`pic_score` (`group_uuid`, `uuid`, `auditor_name`, `score`) values ('1', '2', '3', '4');");

    // echo "<hr>";
    $pic_flag = false;
    foreach($_POST as $k=>$v){
        // var_dump($k);
        // // print_r($v);
        if($k=="group_uuid"){
            $pic_group_uuid = $v;
        }

        $key = explode("_", $k);
        if($key[0] == "score"){
            $pic_uuid = $key[1];
            $pic_uuid_score = $v;

            if ($pic_flag==false){
                $pic_score = array($pic_uuid=>$pic_uuid_score);

                $pic_flag = true;
            }else{
                $pic_score[$pic_uuid]=$pic_uuid_score;
            }
            
        }
    
    }

    $pic_auditor = $_SESSION['auditor'];
    // var_dump($pic_auditor);
    foreach($pic_score as $k=>$v){
        $result = mysqli_query($con, "insert into `pic`.`pic_score` (`group_uuid`, `uuid`, `auditor_name`, `score`) values ('$pic_group_uuid', '$k', '$pic_auditor', '$v');");
    }
    


    mysqli_close($con);
}








// 后端程序处理部分
// 程序入口

session_start();
if(!isset($_SESSION['auditor'])){
    $_SESSION['views']=0;
    $_SESSION['queried_group_uuid']=array();
}

if(isset($_POST["auditor_name"]) && !isset($_SESSION['auditor'])){
    $_SESSION['auditor'] = $_POST["auditor_name"];
}

$session_views = $_SESSION['views'];
print_pic_form($session_views);



// 如果审计员提交表单，处理数据存储
if (isset($_POST['group_uuid']) && isset($_SESSION['auditor']) && (count($_POST)>=3)){
    get_pic_score();
    $_SESSION['views'] = $_SESSION['views'] + 1;
    $views = $_SESSION['views'];
    echo "已做组数: $views";
}

// if(isset())
// var_dump($_GLOBALS);

// echo "<br>POST<br>";
// var_dump($_POST);
// echo "<br>SESSION<br>";
// var_dump($_SESSION);
// if($_SESSION['views']==1){

// }

?>