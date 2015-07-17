<!doctype html>

<html>
<head>

<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width"/>

<link rel="icon" 
      type="image/png" 
      href="" />

<title>Facts Beach :: User</title>

<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href='/css/materialize/css/materialize.min.css' rel='stylesheet' type='text/css'>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<script type="text/javascript" src="/css/materialize/js/materialize.min.js"></script>

<script language="javascript" type="text/javascript" src="/scripts/vendor/jqplot/jquery.jqplot.min.js"></script>
<link rel="stylesheet" type="text/css" href="/scripts/vendor/jqplot/jquery.jqplot.css" />
<script type="text/javascript" src="/scripts/vendor/jqplot/plugins/jqplot.pieRenderer.min.js"></script>
<script type="text/javascript" src="/scripts/vendor/jqplot/plugins/jqplot.donutRenderer.min.js"></script>
<script type="text/javascript" src="/scripts/vendor/jqplot/plugins/jqplot.highlighter.min.js"></script>


<style type="text/css">
    
table.jqplot-table-legend {
  width: auto !important;
}

.expanded-btn {
    width:100%;
}

</style>

</head>

<body>


<nav>
    <div class="nav-wrapper">
      <a href="/" class="brand-logo"><i class="material-icons left">blur_on</i>Facts Beach</a>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        %if logged_in != None:
        <li><a href="/u/account">Home</a></li>
        <li><a href="/logout">Logout</a></li>
        %endif
      </ul>
    </div>
</nav>


<p>&nbsp</p>


<div class="container">

    <p>&nbsp</p>
    <h3><i class="material-icons">insert_chart</i> Reports</h3>

    %for uer in defined_ue_reports:
    <div class="row">
        <div class="col s12 m6">
            <div class="card blue-grey darken-2 duer-card">
                <div class="card-content white-text">
                    <span class="card-title">${uer.name}</span>
                    <p></p>
                </div>
                <div class="card-action">
                    <a href="#" class="delete-uer-filter" data-uer-filter-key="${uer.key}"><i class="material-icons">delete</i></a>
                    <a href="#" class="edit-uer-filter" data-uer-filter-id="${uer.id}"><i class="material-icons">edit</i></a>
                    <a href="#" class="edit-uer-launch" data-uer-filter-id="${uer.id}"><i class="material-icons">launch</i></a>
                </div>
            </div>
        </div>
    </div>
    %endfor


    <p>&nbsp</p>
    <p>&nbsp</p>


    <hr>
    <p>&nbsp</p>
    <h3><i class="material-icons">map</i> Locations</h3>

    <div class="row">
        <div class="col s12">
            <table>
                <thead>
                    <th data-field="name">Name</th>
                    <th data-field="x">X</th>
                    <th data-field="y">Y</th>
                    <th data-field="edit-btn"> </th>
                    <th data-field="delete-btn"> </th>
                </thead>
                <tbody>
                    %for gl in game_locations:
                        %if gl.name != 'world' and gl.id != 1:
                        <tr>
                            <td>${gl.name}</td>
                            <td>${gl.x_point}</td>
                            <td>${gl.y_point}</td>
                            <td>
                                <a class="waves-effect waves-light btn edit-game-loc-btn"
                                    data-game-loc-id=${gl.id}><i class="material-icons">edit</i>
                                </a>
                            </td>
                            <td>
                                <a class="waves-effect waves-light btn delete-game-loc-btn"
                                    data-game-loc-key=${gl.key}><i class="material-icons">remove_circle</i>
                                </a>
                            </td>
                        </tr>
                        %endif
                    %endfor
                </tbody>
            </table>
        </div>
    </div>

</div>



<!-- Modal Structure -->
<div id="new-game-location-modal" class="modal modal-fixed-footer">
    <br>
    <div class="container" style="width:90%;">

        <div class="row">
            <h4>Game Location</h4>
        </div>

        <div class="row">

            <form id="new-game-location-form" method="POST">

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="name", 
                            id_="game-location-name",
                            required=True
                        )
                    }
                    <label id="game-location-name-label" for="game-location-name">Name</label>
                </div>

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="x_point", 
                            id_="game-location-x-point",
                            required=True
                        )
                    }
                    <label id="game-location-x-point-label" for="game-location-x-point">X Point</label>
                </div>

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="y_point", 
                            id_="game-location-y-point",
                            required=True
                        )
                    }
                    <label id="game-location-y-point-label" for="game-location-y-point">Y Point</label>
                </div>
            </form>
        </div>

    </div>

    <div class="modal-footer">
        <a href="#!" class="modal-action waves-effect waves-green btn-flat accept-new-game-location-btn">Save</a>
        <a href="#!" class="modal-action waves-effect waves-red btn-flat no-thanks-new-game-location-btn">Cancel</a>
    </div>
</div>




<!-- <a class="btn-floating btn-large waves-effect waves-light red modal-trigger" data-target="new-defined-ue-report-modal"
    id="new-defined-ue-report-btn" href="#"><i class="material-icons">add</i></a> -->


 <div class="fixed-action-btn" style="bottom: 45px; right: 24px;">
    <a class="btn-floating btn-large red">
      <i class="large material-icons">add</i>
    </a>
    <ul>
        <li><a class="btn-floating amber" id="user-event-modal-btn"><i class="material-icons">add_box</i></a></li>
        <li><a class="btn-floating teal" id="new-game-location-btn"><i class="material-icons">map</i></a></li>
        <li><a class="btn-floating blue-grey" id="new-defined-ue-report-btn"><i class="material-icons">insert_chart</i></i></a></li>
    </ul>
  </div>



<!-- Modal Structure -->
<div id="new-defined-ue-report-modal" class="modal modal-fixed-footer">
    <br>
    <div class="container" style="width:90%;">

        <div class="row">
            <h4>Report</h4>
        </div>

        <div class="row">

            <form id="new-defined-ue-report-form" method="POST">

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="name", 
                            id_="duer-name",
                            required=True
                        )
                    }
                    <label id="duer-name-label" for="session">Name</label>
                </div>

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="session_key", 
                            id_="duer-session-key",
                            required=False
                        )
                    }
                    <label id="duer-session-key-label" for="duer-session-key">Session Key</label>
                </div>

                <p>&nbsp</p>

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="event_category", 
                            id_="duer-event-category",
                            required=True
                        )
                    }
                    <label id="duer-event-category-label" for="event-name">Event Category</label>
                </div>

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="event_metric", 
                            id_="duer-event-metric",
                            required=True
                        )
                    }
                    <label id="duer-event-metric-label" for="event-metric">Event Metric</label>
                </div>

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="event_value", 
                            id_="duer-event-value",
                            required=True
                        )
                    }
                    <label id="duer-event-label" for="event-value">Event Value</label>
                </div>

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="output_chart_name", 
                            id_="duer-output-chart-name",
                            required=True
                        )
                    }
                    <label id="duer-output-chart-name-label" for="event-value">Chart Name (Optional)</label>
                </div>

                <input type="hidden" id="duer-id" name="id" value=""/>

            </form>
        </div>

    </div>

    <div class="modal-footer">
        <a href="#!" class="modal-action waves-effect waves-green btn-flat accept-new-defined-ue-report-btn">Save</a>
        <a href="#!" class="modal-action waves-effect waves-red btn-flat no-thanks-new-defined-ue-report-btn">Cancel</a>
    </div>
</div>



<!-- Modal Structure -->
<div id="user-event-modal" class="modal modal-fixed-footer">
    <div class="modal-content">

        <div class="row">
            <h4>User Event</h4>
        </div>
        

        <div class="row">

            <form id="user-event-form" method="POST">

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="session_key", 
                            id_="session-key",
                            required=True
                        )
                    }
                    <label for="session">Session Key</label>
                </div>

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="event_category", 
                            id_="event-category",
                            required=True
                        )
                    }
                    <label for="event-name">Event Category</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="event_metric", 
                            id_="event-metric",
                            required=True
                        )
                    }
                    <label for="event-metric">Event Metric</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="event_value", 
                            id_="event-value",
                            required=True
                        )
                    }
                    <label for="event-value">Event Value</label>
                </div>

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="game_location_name", 
                            id_="game-location-name",
                            required=False
                        )
                    }
                    <label for="game-location-name">Location Name</label>
                </div>

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="in_game_timestamp", 
                            id_="in-game-timestamp",
                            required=True
                        )
                    }
                    <label for="in-game-timestamp">In-Game Timestamp</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="build_number", 
                            id_="build-number",
                            required=True
                        )
                    }
                    <label for="build-number">Build Number</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="head_health", 
                            id_="head-health",
                            required=True
                        )
                    }
                    <label for="head-health">Head Health</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="torso_health", 
                            id_="torso-health",
                            required=True
                        )
                    }
                    <label for="torso-health">Torso Health</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="right_arm_health", 
                            id_="right-arm-health",
                            required=True
                        )
                    }
                    <label for="right-arm-health">Right Arm Health</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="left_arm_health", 
                            id_="left-arm-health",
                            required=True
                        )
                    }
                    <label for="left-arm-health">Left Arm Health</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="left_leg_health", 
                            id_="left-leg-health",
                            required=True
                        )
                    }
                    <label for="left-leg-health">Left Leg Health</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="right_leg_health", 
                            id_="right-leg-health",
                            required=True
                        )
                    }
                    <label for="right-leg-health">Right Leg Health</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="mental_health", 
                            id_="mental-health",
                            required=True
                        )
                    }
                    <label for="mental-health">Mental Health</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="stamina", 
                            id_="stamina",
                            required=True
                        )
                    }
                    <label for="stamina">Stamina</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="oxygen", 
                            id_="oxygen",
                            required=True
                        )
                    }
                    <label for="oxygen">Oxygen</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="food", 
                            id_="food",
                            required=True
                        )
                    }
                    <label for="food">Food</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="water", 
                            id_="water",
                            required=True
                        )
                    }
                    <label for="water">Water</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="temperature", 
                            id_="temperature",
                            required=True
                        )
                    }
                    <label for="temperature">Temperature</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="total_health", 
                            id_="total-health",
                            required=True
                        )
                    }
                    <label for="total-health">Total Health</label>
                </div>

                <p>&nbsp</p>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="os_name", 
                            id_="os-name",
                            required=True
                        )
                    }
                    <label for="os-name">OS Name</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="cpu_name", 
                            id_="cpu-name",
                            required=True
                        )
                    }
                    <label for="cpu-name">CPU Name</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="gpu_name", 
                            id_="gpu-name",
                            required=True
                        )
                    }
                    <label for="gpu-name">GPU Name</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="gmem_size", 
                            id_="gmem-size",
                            required=True
                        )
                    }
                    <label for="gmem-size">G Memory Sz</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="smem_size", 
                            id_="smem-size",
                            required=True
                        )
                    }
                    <label for="smem-size">S Memory Sz</label>
                </div>

                <div class="input-field col s6">
                    ${
                        pymf.add_input(
                            "number", 
                            name_="frame_rate", 
                            id_="frame-rate",
                            required=True
                        )
                    }
                    <label for="frame-rate">Frame Rate</label>
                </div>

                <div class="input-field col s12">
                    ${
                        pymf.add_input(
                            "text", 
                            name_="resolution", 
                            id_="resolution",
                            required=True
                        )
                    }
                    <label for="resolution">Resolution</label>
                </div>


                <p>&nbsp</p>

                <div class="input-field col s6">

                    <input type="hidden" name="resp" value="html"/>
                    <input type="hidden" name="app_name" value="Hevn Online" />
                    <input type="hidden" name="device_token" value="BROWSER_DEVICE_TOKEN" />

                </div>

            </form>

        </div>

    </div>
    <div class="modal-footer">
        <a href="#!" 
            id="user-event-modal-post-btn"
            class="modal-action waves-effect waves-green btn-flat ">Post</a>
    </div>
</div>



</body>

<script type="text/javascript">

$(document).ready(function(){

    $('.modal-trigger').leanModal({
        opacity: .1
    });


    $("#new-defined-ue-report-btn").click(function(event){
        event.preventDefault();
        $(".accept-new-defined-ue-report-btn").removeAttr('data-uer-filter-id');
        $("#new-defined-ue-report-modal").openModal();

    });


    $(".accept-new-defined-ue-report-btn").click(function(event){
        event.preventDefault();

        var form = $("form[id=new-defined-ue-report-form]");
        var data = form.serializeArray();

        var action = "PUT";
        var duer_id = $(this).attr('data-uer-filter-id');
        if(typeof duer_id === 'undefined'){
            action = "POST";
        }else{
            data.push({'name':'id', 'value':duer_id});
        }

        $.ajax({
            type:action,
            url:"/m/edit/DefinedUserEventReport",
            data:data,
            success:function(data){
                window.location.reload(false);
            },
            error:function(data){
                alert('Error');
            }
        });

        $("#new-defined-ue-report-modal").closeModal();

    });

    $(".no-thanks-new-defined-ue-report-btn").click(function(event){
        $("#new-defined-ue-report-modal").closeModal();

    });

    $(".edit-uer-filter").click(function(event){
        event.preventDefault();
        var duer_id = $(this).attr('data-uer-filter-id');

        $.ajax({
            'type':'GET',
            'url':'/m/edit/DefinedUserEventReport/id='+duer_id,
            success:function(data){
                console.log(data.results[0]);

                $("#duer-name").val(data.results[0].name);
                $("#duer-name-label").addClass('active');
                $("#duer-session-key").val(data.results[0].session_key);
                $("#duer-session-key-label").addClass('active');
                $("#duer-event-category").val(data.results[0].event_category);
                $("#duer-event-category-label").addClass('active');
                $("#duer-event-metric").val(data.results[0].event_metric);
                $("#duer-event-metric-label").addClass('active');
                $("#duer-event-value").val(data.results[0].event_value);
                $("#duer-event-label").addClass('active');
                $("#duer-output-chart-name").val(data.results[0].output_chart_name);
                $("#duer-output-chart-name-label").addClass('active');

                $('.accept-new-defined-ue-report-btn').attr('data-uer-filter-id', data.results[0].id);

                $("#new-defined-ue-report-modal").openModal();
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log('Error');
            }
        });

    });

    $(".delete-uer-filter").click(function(event){

        var duer_key = $(this).attr('data-uer-filter-key');

        console.log('Delete UER report clicked ' + duer_key);

        $.ajax({
            'type':'DELETE',
            'url':'/m/edit/DefinedUserEventReport',
            'data': {
                key:duer_key
            },
            success:function(data){
                window.location.reload(false);
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log('Error');
            }
        });

    });


    $(".edit-uer-launch").click(function(event){
       event.preventDefault();
       var duer_id = $(this).attr('data-uer-filter-id');
       window.location.href = '/r/base-report/id='+duer_id;
    });


    $("#user-event-modal-btn").click(function(event){
        $('#user-event-modal').openModal();
    });

    $("#user-event-modal-post-btn").click(function(event){
        event.preventDefault();

        var form = $("form[id=user-event-form]");
        var data = form.serializeArray();

        console.log(data);

        $.ajax({
            type:"POST",
            url:"/m/edit/UserEvent",
            data:data,
            success:function(data){
                window.location.reload(false);
            },
            error:function(data){
                alert('Error');
            }
        });
    });


    $("#new-game-location-btn").click(function(event){
        $('#new-game-location-modal').openModal();
    });


    $(".edit-game-loc-btn").click(function(event){
        console.log('edit-game-loc-btn');
        event.preventDefault();
        var gl_id = $(this).attr('data-game-loc-id');

        $.ajax({
            'type':'GET',
            'url':'/m/edit/GameLocationTypeLookup/id='+gl_id,
            success: function(data){
                $("#game-location-name").val(data.results[0].name);
                $("#game-location-name-label").addClass('active');
                $("#game-location-x-point").val(data.results[0].x_point);
                $("#game-location-x-point-label").addClass('active');
                $("#game-location-y-point").val(data.results[0].y_point);
                $("#game-location-y-point-label").addClass('active');
                $(".accept-new-game-location-btn").attr('data-game-loc-id', gl_id);

                $("#new-game-location-modal").openModal();
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log('Error');
            }
        });

    });

    $(".accept-new-game-location-btn").click(function(event){
        event.preventDefault();

        var form = $("form[id=new-game-location-form]");
        var data = form.serializeArray();

        var action = "PUT";
        var gl_id = $(this).attr('data-game-loc-id');
        if(typeof gl_id === 'undefined'){
            action = "POST";
        }else{
            data.push({'name':'id', 'value':gl_id});
        }

        $.ajax({
            type:action,
            url:"/m/edit/GameLocationTypeLookup",
            data:data,
            success:function(data){
                window.location.reload(false);
            },
            error:function(data){
                alert('Error');
            }
        });

        $("#new-game-location-modal").closeModal();

    });

    $(".no-thanks-new-game-location-btn").click(function(event){
        $("#new-game-location-modal").closeModal();
    });


    $(".delete-game-loc-btn").click(function(event){
        event.preventDefault();
        var gl_key = $(this).attr("data-game-loc-key");

        alert(gl_key);

        $.ajax({
            type:"DELETE",
            url:"/m/edit/GameLocationTypeLookup",
            data:{
                key:gl_key
            },
            success:function(data){
                window.location.reload(false);
            },
            error:function(data){
                alert('Error');
            }
        });

    });


    $(".duer-card").hover(
        function(){
            $(this).addClass("z-depth-2");
            $(this).addClass("darken-1");
            $(this).removeClass("darken-2");
        },
        function(){
            $(this).removeClass("z-depth-2");
            $(this).addClass("darken-2");
            $(this).removeClass("darken-1");
        }
    );


});  



</script>
</html>

<%namespace name="pymf" file="modelfuncs.mako"/>























