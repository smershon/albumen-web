$(document).ready(function(){

    var select_uid = null;   
 
    $("#commit_button").bind("click", function() {
        $("#album_info").html($("#loading-gif").text());
        $.post("/albumen/search", {
            "artist": $("#artist_input").val(),
            "album": $("#album_input").val() 
            },
            function(response) {
                data = response.data
                console.log(data);
                $("#album_info").html(_.template($("#album_template").html(), { results : data.length }));

                _.each(data, function(album, idx, lst) {
                    var img = new Image();

                    img.onload = function() {
                        $("#album_table tbody").append(_.template($("#image_row").html(),
                            {album: album, width: img.width, height: img.height}));
                        $("#album_info tr").click(function() {
                            select_uid = $(this).attr('id')
                            $("#album_info tr").css('background-color', 'white');
                            $(this).css('background-color', '#FFCF00');
                            $("#save_button").attr("disabled", false);
                        });
                    };

                    img.src = album.image.url;
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
            "artist" : $("#" + select_uid + " #artist_name").html(),
            "album" : $("#" + select_uid + " #album_name").html(),
            "image_url" : $("#" + select_uid + " #img_url").html()
            },
            function(data) {
                console.log(data);
                $("#save_button").attr("disabled", "disabled");
        });
    });

});

