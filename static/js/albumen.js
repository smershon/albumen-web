$(document).ready(function(){

    var select_uid = null;   
 
    $("#commit_button").bind("click", function() {
        search();
    })

    function search() {
        $("#album_info").html($("#loading-gif").text());
        $.post("/albumen/search", {
            "artist": $("#artist_input").val(),
            "album": $("#album_input").val() 
            },
            function(response) {
                $("#album_info").html(_.template($("#album_template").html(), { results : response.images.length }));

                _.each(response.albums, function(album, idx, lst) {
                    $("#album_table tbody").append(_.template($("#album_row").html(), {album: album}))
                });

                _.each(response.images, function(album, idx, lst) {
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
        
                        $("#album_info tr #supplied_url").click(function() {
                            var uid = $(this).parent().parent().parent().attr("id");
                            var supplied_url = $("#" + uid + " #supplied_url_input").val();
                            if(supplied_url) {
                                var img = new Image();

                                img.onload = function() {
                                    var tmpl = {
                                        artist: $("#" + uid + " #artist_name").html(),
                                        album: $("#" + uid + " #album_name").html(),
                                        url: supplied_url,
                                        width: img.width,
                                        height: img.height
                                    }
                                    $("#" + uid).html(_.template($("#image_row_inner").html(), tmpl));
                                }

                                img.src = supplied_url;
                            }
                        });

                    };

                    img.src = album.image.url;
                });
            }
        );
    }

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

    var artist_input = $("#artist_input").val();
    var album_input = $("#album_input").val();

    if(artist_input && album_input) {
        search();
    }

});

