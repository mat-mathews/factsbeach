<!doctype html>

<html>
<head>

<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width"/>

<link rel="icon" 
	  type="image/png" 
	  href="" />

<title>Facts Beach :: Report</title>

<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href='/css/materialize/css/materialize.min.css' rel='stylesheet' type='text/css'>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<script type="text/javascript" src="/css/materialize/js/materialize.min.js"></script>

<script language="javascript" type="text/javascript" src="/scripts/vendor/jqplot/jquery.jqplot.min.js"></script>
<link rel="stylesheet" type="text/css" href="/scripts/vendor/jqplot/jquery.jqplot.css" />
<script type="text/javascript" src="/scripts/vendor/jqplot/plugins/jqplot.pieRenderer.min.js"></script>
<script type="text/javascript" src="/scripts/vendor/jqplot/plugins/jqplot.donutRenderer.min.js"></script>
<script type="text/javascript" src="/scripts/vendor/jqplot/plugins/jqplot.highlighter.min.js"></script>
<script type="text/javascript" src="/scripts/vendor/jqplot/plugins/jqplot.bubbleRenderer.min.js"></script>


<style type="text/css">
	
table.jqplot-table-legend {
  width: auto !important;
}

#new-defined-ue-report-btn{
  margin-left: 20px;
  vertical-align: baseline;
  position: absolute;
  right: 24px;
  bottom: 24px;
  opacity: .9;
}

#render-snd-btn{
	top: 27px;
}

.expanded-btn {
    width:100%;
}

</style>

</head>

<body>


<nav>
	<div class="nav-wrapper">
	  <a href="#" class="brand-logo"><i class="material-icons left">blur_on</i>Facts Beach</a>
	  <ul id="nav-mobile" class="right">
		%if logged_in != None:
		<li><a href="/u/account">Home</a></li>
		<li><a href="/logout">Logout</a></li>
		%endif
	  </ul>
	</div>
</nav>


<p>&nbsp</p>


<div class="container">

	<div class="row">
		<div class="valign-wrapper">
			<div class="col s4 valign">
				<h4>Session</h4>
			</div>
			<div class="col s8 valign">
			<select id="select-session">
				%for sk in session_keys:
					%if sk[0] == duer.session_key:
					<option value="${sk[0]}" selected>${sk[0]}</option>
					%else:
					<option value="${sk[0]}">${sk[0]}</option>
					%endif
				%endfor
			</select>
			</div>
		</div>
	</div>

	<p>&nbsp</p>

    <p>&nbsp</p>
    <h4><i class="material-icons">widgets</i> Specs</h4>

    <div class="row">
        <div class="col s12">
            <table>
                <thead>
                	<th data-field="os_name">OS</th>
                    <th data-field="cpu_name">CPU</th>
                    <th data-field="gpu_name">GPU</th>
                    <th data-field="gmem_size">GMEM</th>
                    <th data-field="smem_size">SMEM</th>
                </thead>
                <tbody>
	                <tr>
	                    <td id="data-os-name"></td>
	                    <td id="data-cpu-name"></td>
	                    <td id="data-gpu-name"></td>
	                    <td id="data-gmem-size"></td>
	                    <td id="data-smem-size"></td>
	                </tr>
                </tbody>
            </table>
        </div>
    </div>

    <p>&nbsp</p>

	<div class="row">
		<div id="chartdiv" style="height:400px;width:100%;top:5px;">

			<div class="preloader-wrapper big active">
				<div class="spinner-layer spinner-blue-only">
				  <div class="circle-clipper left">
				    <div class="circle"></div>
				  </div><div class="gap-patch">
				    <div class="circle"></div>
				  </div><div class="circle-clipper right">
				    <div class="circle"></div>
				  </div>
				</div>
			</div>

		</div>
	</div>

	<p>&nbsp</p>

	<div class="row">
		<div id="attributes-chart" style="height:400px;width:100%;top:5px;"></div>
	</div>

	<p>&nbsp</p>

	<div class="row">
		<div id="perf-chart" style="height:400px;width:100%;top:5px;"></div>
	</div>

	<p>&nbsp</p>

	<div class="row">
		<!-- <h4>Locations</h4> -->
		<div id="location-chart" style="height:400px;width:100%;top:5px;"></div>
	</div>

	<p>&nbsp</p>
	<p>&nbsp</p>



	<div class="divider"></div>
	<p>&nbsp</p>


	<div class="row">
		<div class="col s6">
			<h4>Chart User Event</h4>
		</div>
		<div class="col s2 offset-s4">
			<a class="waves-effect waves-light btn right-aligned" id="render-snd-btn">Render</a>
		</div>
	</div>

	<div class="row">

		<div class="input-field col s12 m4">
			<select id="select-snd-cat">
				<option value="" disabled selected>Category</option>
				%for ue_cat in ue_cats:
					<option value="${ue_cat}">${ue_cat}</option>
				%endfor
			</select>
		</div>

		<div class="input-field col s12 m4">
			<select id="select-snd-met">
				<option value="" disabled selected>Metric</option>
				%for ue_met in ue_mets:
					<option value="${ue_met}">${ue_met}</option>
				%endfor
			</select>
		</div>

		<div class="input-field col s12 m4">
			<select id="select-snd-val">
				<option value="" disabled selected>Value</option>
				%for ue_val in ue_vals:
					<option value="${ue_val}">${ue_val}</option>
				%endfor
			</select>
		</div>

	</div>

	<div class="row">
		<div id="snd-metric-chart" style="height:400px;width:100%;top:5px;">Select metrics and values to render</div>
	</div>


	<p>&nbsp</p>
    <h3><i class="material-icons">track_changes</i> Game Play Events</h3>

    <div class="row">
        <div class="col s12">
            <table>
                <thead>
                    <th data-field="name">Name</th>
                    <th data-field="name">Activated</th>
                </thead>
                <tbody>
                    %for gl in game_play_events:
                        %if gl.name != 'na' and gl.id != 1:
                        <tr>
                            <td>${gl.name}</td>
                            %if gl.name in ue_vals:
                            	<td>Yes</td>
                            %else:
                            	<td>No</td>
                            %endif
                        </tr>
                        %endif
                    %endfor
                </tbody>
            </table>
        </div>
    </div>


</div>

</body>

<script type="text/javascript">

$(document).ready(function(){


	$('select').material_select();

	function load_session_data(session_key){

		console.log('load_session_data called');

		$.ajax({
			type:"GET",
			url:"/r/base/event_category=${duer.event_category}/event_metric=${duer.event_metric}/event_value=${duer.event_value}/session_key="+session_key,
			success:function(data){

				console.log(data);


				$("#data-os-name").html(data.os_name);
				$("#data-cpu-name").html(data.cpu_name);
				$("#data-gpu-name").html(data.gpu_name);
				$("#data-gmem-size").html(data.gmem_size);
				$("#data-smem-size").html(data.smem_size);


				var headPoints = [];
				for (var i=0; i<data.head_health.length; i+=1){ 
					headPoints.push([data.head_health[i][0], data.head_health[i][1]]);
				}

				var torsoPoints = [];
				for (var i=0; i<data.torso_health.length; i+=1){ 
					torsoPoints.push([data.torso_health[i][0], data.torso_health[i][1]]);
				}

				var rightArmPoints = [];
				for (var i=0; i<data.right_arm_health.length; i+=1){ 
					rightArmPoints.push([data.right_arm_health[i][0], data.right_arm_health[i][1]]); 
				}

				var leftArmPoints = [];
				for (var i=0; i<data.left_arm_health.length; i+=1){ 
					leftArmPoints.push([data.left_arm_health[i][0], data.left_arm_health[i][1]]); 
				}

				var rightLegPoints = [];
				for (var i=0; i<data.right_leg_health.length; i+=1){ 
					rightLegPoints.push([data.right_leg_health[i][0], data.right_leg_health[i][1]]); 
				}

				var leftLegPoints = [];
				for (var i=0; i<data.left_leg_health.length; i+=1){ 
					leftLegPoints.push([data.left_leg_health[i][0], data.left_leg_health[i][1]]); 
				}

				var totalHealthPoints = [];
				for (var i=0; i<data.total_health.length; i+=1){ 
					totalHealthPoints.push([data.total_health[i][0], data.total_health[i][1]]); 
				}

				// and for attributes graph


				var mentalHealthPoints = [];
				for (var i=0; i<data.mental_health.length; i+=1){ 
					mentalHealthPoints.push([data.mental_health[i][0], data.mental_health[i][1]]); 
				}

				var staminaPoints = [];
				for (var i=0; i<data.stamina.length; i+=1){ 
					staminaPoints.push([data.stamina[i][0], data.stamina[i][1]]); 
				}

				var oxygenPoints = [];
				for (var i=0; i<data.oxygen.length; i+=1){ 
					oxygenPoints.push([data.oxygen[i][0], data.oxygen[i][1]]); 
				}

				var foodPoints = [];
				for (var i=0; i<data.food.length; i+=1){ 
					foodPoints.push([data.food[i][0], data.food[i][1]]); 
				}

				var waterPoints = [];
				for (var i=0; i<data.water.length; i+=1){ 
					waterPoints.push([data.water[i][0], data.water[i][1]]); 
				}

				var temperaturePoints = [];
				for (var i=0; i<data.temperature.length; i+=1){ 
					temperaturePoints.push([data.temperature[i][0], data.temperature[i][1]]); 
				}

				var frameRatePoints = [];
				for (var i=0; i<data.frame_rate.length; i+=1){ 
					frameRatePoints.push([data.frame_rate[i][0], data.frame_rate[i][1]]); 
				}

				var resolutionPoints = [];
				for (var i=0; i<data.resolution.length; i+=1){ 
					resolutionPoints.push([data.resolution[i][0], data.resolution[i][1]]); 
				}

				$("#chartdiv").html("");
				$("#attributes-chart").html("");
				$("#perf-chart").html("");

				try{
									
					// var plot3 = $.jqplot('chartdiv', [headPoints, torsoPoints, rightArmPoints, leftArmPoints, rightLegPoints, leftLegPoints], 
					var plot3 = $.jqplot('chartdiv', [headPoints, torsoPoints, rightArmPoints, leftArmPoints, rightLegPoints, leftLegPoints, totalHealthPoints], 
					{ 
						title:'Health', 

						legend: { show: true, location: "w" },

						series:[ 
							{
								label:"Head",
								markerOptions: { style:'circle' }
							}, 
							{
								label:"Torso",
								markerOptions: { style:"circle" }
							},
							{ 
								label:"Rt. Arm",
								markerOptions: { style:"circle" }
							}, 
							{
								label:"Lf. Arm",
								markerOptions: { style:"circle" }
							},
							{
								label:"Rt. Leg",
								markerOptions: { style:"circle" }
							},
							{
								label:"Lt. Leg",
								markerOptions: { style:"circle" }
							},
							{
								label:"Total Health",
								markerOptions: { style:"circle" }
							}
						],

					});

				}catch(e){
					$("#chartdiv").html("No Health Data");
				}


				try{

					var plot4 = $.jqplot('attributes-chart', [mentalHealthPoints, staminaPoints, oxygenPoints, foodPoints, waterPoints, temperaturePoints], 
					{ 
						title:'Attributes', 

						legend: { show: true, location: "w" },

						series:[ 
							{
								label:"Mental",
								markerOptions: { style:'circle' }
							}, 
							{
								label:"Stamina",
								markerOptions: { style:"circle" }
							},
							{ 
								label:"O2",
								markerOptions: { style:"circle" }
							}, 
							{
								label:"Food",
								markerOptions: { style:"circle" }
							},
							{
								label:"H2O",
								markerOptions: { style:"circle" }
							},
							{
								label:"Temp",
								markerOptions: { style:"circle" }
							}
						],

					});

				}catch(e){
					$("#attributes-chart").html("No Attributes Data");
				}


				try{

					var plot5 = $.jqplot('perf-chart', [frameRatePoints], 
					{ 
						title:'Performance', 

						legend: { show: true, location: "w" },

						series:[ 
							{
								label:"FrameRate",
								markerOptions: { style:'circle', size:'20' }
							}
						],

					});

				}catch(e){
					$("#perf-chart").html("No Perf Data");
				}


			},
			error:function(){
				alert('Error');
			}
		});



		$.ajax({
			type:"GET",
			url:"/r/game-loc",
			success:function(data){

				var arr = [];
				$.each(Object.keys(data.game_locations), function(i, v){

					if(v != "world"){
						arr.push([data.game_locations[v].points[0], data.game_locations[v].points[1], data.game_locations[v].count*2, v]);
					}
					
				});

				var plot1 = $.jqplot('location-chart',[arr],{
					title: 'Player Location/Frequency',
					seriesDefaults:{
						renderer: $.jqplot.BubbleRenderer,
						rendererOptions: {
							bubbleGradients: true,
							bubbleAlpha: 0.5
						},
						shadow: true
					}
				});
			},
			error:function(){
				alert('Error');
			}
		});




	}

	$("#select-session").change(function(event){
		var session_key = $(this).find(":selected").val();
		load_session_data(session_key);
	});


	$("#render-snd-btn").click(function(event){
		var cat = $("#select-snd-cat option:selected").val();
		var met = $("#select-snd-met option:selected").val();
		var val = $("#select-snd-val option:selected").val();

		$("#snd-metric-chart").html("");

		var session_key = $("#select-session").find(":selected").val();

		$.ajax({
			type:"GET",
			url:"/r/compare/event_category="+cat+"/event_metric="+met+"/event_value="+val+"/session_key="+session_key,
			success: function(data){
				var valPoints = [];
				for (var i=0; i<data.event_values.length; i+=1){ 
					valPoints.push([data.event_values[i][0], data.event_values[i][1]]); 
				}

				var plot5 = $.jqplot('snd-metric-chart', [valPoints], 
				{ 
					title:'Compare Metric Values', 

					legend: { show: true, location: "w" },

					series:[ 
						{
							label:data.val_name,
							markerOptions: { style:'circle' }
						}
					],

					axes: {
						yaxis: {min: 0, max: 2, numberTicks:2},
					}

				});

			},
			error: function(){
				alert("Error");
			}

		});


	});

	var session_key = $("#select-session").find(":selected").val();
	load_session_data(session_key);

});

</script>

</html>


<%namespace name="pymf" file="modelfuncs.mako"/>









