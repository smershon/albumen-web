$(document).ready(function(){

    var select_uid = null;   
 
    $("#commit_button").bind("click", function() {
        $("#album_info").html($("#loading-gif").text());
        $.post("/albumen", {
            "artist": $("#artist_input").val(),
            "album": $("#album_input").val() 
            },
            function(data) {
                $("#album_info").html(_.template($("#album_template").html(), { album : data }));

                _.each(data["images"], function(img_url, idx, lst) {
                    var img = new Image();

                    img.onload = function() {
                        $("#album_table tbody").append(_.template($("#image_row").html(),
                            {img_url: img_url, width: img.width, height: img.height}));
                        $("#album_info tr").click(function() {
                            select_uid = $(this).attr('id')
                            $("#album_info tr").css('background-color', 'white');
                            $(this).css('background-color', '#FFCF00');
                            $("#save_button").removeAttr("disabled");
                        });
                    };

                    img.src = img_url.url;
                });
            }
        );
    });

    $("#save_button").click( function() {
        if(!select_uid) {
            return;
        }
        console.log("SAVING");
        $.post("/albumen/save", {
            "artist" : $("#artist_input").val(),
            "album" : $("#album_input").val(),
            "image_url" : $("#" + select_uid + " td:first p:first").html()
            },
            function(data) {
                console.log(data);
                $("#save_button").attr("disabled", "disabled");
        });
    });

});

