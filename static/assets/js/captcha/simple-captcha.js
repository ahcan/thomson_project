// add <div class="simple-captcha"> to use captcha
$(document).ready(function(){
        renderLayout($('.simple-captcha'));
        // $('#form-1').submit(function(e){e.preventDefault();});
});
function renderLayout(list_div){
    for (var i = list_div.length - 1; i >= 0; i--) {
            createCaptcha(list_div[i].id);
            loadCaptcha(list_div[i].id);
    }
}
function loadCaptcha(ele_id){
    $.ajax({url:"/system/captcha/", 
        type:"GET",dataType:"JSON", 
        contentType:'application/json',
        success: function(response){
           setValue(response['new_cptch_key'], response['new_cptch_image'], ele_id);
    }});
}
function setValue(cpt_key, cpt_image, ele_id){
    $("#img-captcha-"+ele_id).attr('src',cpt_image);
    $('#cpt-key-'+ele_id).val(cpt_key);
    $('#cpt-value-'+ele_id).val('');
}
function createCaptcha(ele_id){
    var img = "<img id='img-captcha-"+ele_id+"'></img>";
    var input = "<input id ='cpt-value-"+ele_id+"' name='captcha_1' class='form-control' type='text' placeholder='Type captcha'>";
    var cpt_key = "<input id='cpt-key-"+ele_id+"' type='text'>";
    var validate = "<input type='button' class='btn btn-info btn-sm' onclick='resetCaptcha("+ele_id+")' value='Reset'>";
    var error_lable = "<div id ='error-captcha-"+ele_id+"' class='alert alert-danger'><p id ='error"+ele_id+"'></p></div>";
    $("#"+ele_id).append("<div class='form-inline'>"+error_lable+img+input+cpt_key+validate+"</div>");
    $('#cpt-key-'+ele_id).hide();
    $('#error-captcha-'+ele_id).hide();
}
function resetCaptcha(ele_id){
    var ele_id = ele_id.id;
    $.ajax({url:"/system/captcha",
        type:"GET", dataType:"JSON",
        contentType:'application/json',
        success: function(response){
            setValue(response['new_cptch_key'], response['new_cptch_image'],ele_id);
            $('#error-captcha-'+ele_id).hide();},
    });
}
function valiCaptcha(ele_id){
    var str_error ='';
    // console.log(ele_id);
    var datasent = {'cpt_value':$('#cpt-value-'+ele_id).val(),'cpt_key':$('#cpt-key-'+ele_id).val()};
    if($.trim($('#cpt-value-'+ele_id).val()) == ''){
        str_error = "Input can not be left blank";
        $('#error'+ele_id).text(str_error);
        $('#error-captcha-'+ele_id).show();
        return false;
    }else{
        // console.log(datasent);
        $.ajax({url:"/system/captcha/",
            async: false,
            type:"POST", dataType:"json",
            contentType:'application/json',
            data:JSON.stringify(datasent),
            success: function(response){
                if(response['status']){
                    $('#error'+ele_id).text("Captcha is wrong!");
                    $('#error-captcha-'+ele_id).show();
                    setValue(response['new_cptch_key'], response['new_cptch_image'],ele_id);
                    return false;
                }
                else{
                    $('#error-captcha-'+ele_id).hide();
                    loadCaptcha(ele_id);
                    return true;}
            },
            error: function(response){
                $("#error"+ele_id).text("Not connect server!");
                $('#error-captcha-'+ele_id).show();
                return false;
            },});
    }
}