    $(document).ready(function() {
        socket.on('connect', function(data_) {
            socket.emit('my_event', {data: 'I\'m connected!'});
            // console.log(data_)

            socket.emit("get_my_sid");

        });
        socket.on('my_sid', function(msg, cb) {
            var sid = msg
            $("#canvas").attr("data-sid", sid)
        })
        socket.on('last_vosk_lines', function(msg, cb) {
            $('#vosk_log').html("")
            $.each(msg.data, function(index, line) {
                $('#vosk_log').append('<br>' + $('<div/>').text(line).html());
            })
            if (cb)
                cb();
        });

        socket.on('my_vosk_log', function(msg, cb) {

            $('#vosk_log').append('<br>' + $('<div/>').text(msg.data).html());
            if (cb)
                cb();
        });

        socket.on('my_response_voice', function(msg, cb) {


        })

        socket.on('my_response', function(msg, cb) {
            if(msg.data == "Connected") {
                sid_ = msg.sid
                socket.emit("init_ctrl", {"data": "get_last_vosk_logs"})
            }
            $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
                if($("#form_sid").length > 0) {
                    $("#form_sid").val(btoa(msg["sid"]))
                    console.log($("#form_sid"))
                }
            if (cb)
                cb();
        });

        $('#message').keypress(function (e) {
          if (e.which == 13) {

          if($("#message").val().length > 0) {
                console.log("emitto")
                socket.emit("my_broadcast_event", {data: $("#message").val()})
            } else {
                console.error("no message")
            }

            messages.push($('#message').val())
            messages_last_set_index = messages.length
            $('#message').val('')

          }
        });
    });