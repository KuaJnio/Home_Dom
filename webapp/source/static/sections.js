$(document).ready(function(){
    $(".section_home").hide();
    $(".section_actuators").hide();
    $(".section_status").show();
    
    $(".tab_home").click(function(){
        $(".section_home").fadeIn();
        $(".section_actuators").hide();
        $(".section_status").hide();
    });
    $(".tab_actuators").click(function(){
        $(".section_home").hide();
        $(".section_actuators").fadeIn();
        $(".section_status").hide();
    });
    $(".tab_status").click(function(){
        $(".section_home").hide();
        $(".section_actuators").hide();
        $(".section_status").fadeIn();
    });
});
