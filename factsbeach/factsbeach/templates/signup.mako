<!doctype html>

<html>
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width"/>

    <link rel="icon" 
          type="image/png" 
          href="/assets/mividio_house_bug_small.png" />

	<title>Playmatics :: New User</title>

    <link rel="stylesheet" href="/foundation/css/foundation.css"/>
    <link rel="stylesheet" href="/css/font-awesome/css/font-awesome.min.css">

    <script type="text/javascript" src="/scripts/vendor/jquery-2.0.3.js"></script>
    <script src="/foundation/js/vendor/modernizr.js"></script>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>

</head>

<style>
.ribbon-wrapper-green {
  width: 85px;
  height: 88px;
  overflow: hidden;
  position: absolute;
  top: -3px;
  right: -3px;
}

.ribbon-green {
  font: bold 13px Sans-Serif;
  color: #333;
  text-align: center;
  text-shadow: rgba(255,255,255,0.5) 0px 1px 0px;
  -webkit-transform: rotate(45deg);
  -moz-transform:    rotate(45deg);
  -ms-transform:     rotate(45deg);
  -o-transform:      rotate(45deg);
  position: relative;
  padding: 7px 0;
  left: -5px;
  top: 15px;
  width: 120px;
  background-color: #BFDC7A;
  background-image: -webkit-gradient(linear, left top, left bottom, from(#BFDC7A), to(#8EBF45)); 
  background-image: -webkit-linear-gradient(top, #BFDC7A, #8EBF45); 
  background-image:    -moz-linear-gradient(top, #BFDC7A, #8EBF45); 
  background-image:     -ms-linear-gradient(top, #BFDC7A, #8EBF45); 
  background-image:      -o-linear-gradient(top, #BFDC7A, #8EBF45); 
  color: #6a6340;
  -webkit-box-shadow: 0px 0px 3px rgba(0,0,0,0.3);
  -moz-box-shadow:    0px 0px 3px rgba(0,0,0,0.3);
  box-shadow:         0px 0px 3px rgba(0,0,0,0.3);
}

.ribbon-green:before, .ribbon-green:after {
  content: "";
  border-top:   3px solid #6e8900;   
  border-left:  3px solid transparent;
  border-right: 3px solid transparent;
  position:absolute;
  bottom: -3px;
}

.ribbon-green:before {
  left: 0;
}
.ribbon-green:after {
  right: 0;
}

.switch-assistant {}
</style>

<body>


<p>&nbsp</p>


<div class="row collapse">
    <div class="small-11 small-centered medium-6 medium-centered columns">
      <h1 class="subheader">Playmatics</h1>
    </div>
</div>


<div class="row">

    <div class="small-11 small-centered medium-6 medium-centered columns">

        <div class="row">
            <form id="signup-form" data-abide method="POST">

                <div class="row">
                    <div class="small-12 columns">
                        ${
                            pymf.add_input(
                                "text", 
                                name_="email_address", 
                                id_="email_address",
                                placeholder="Enter your email",
                                required=True, 
                                pattern="email",
                                value=email_address
                            )
                        }
                        <small class="error">A valid email address is required</small>
                    </div>
                </div>

                <div class="row">
                    <div class="small-12 columns">
                        ${
                            pymf.add_input(
                                "password", 
                                name_="password", 
                                id_="password",
                                placeholder="Choose a password",
                                required=True, 
                                pattern="password"
                            )
                        }
                        <small class="error">A strong password is required... at least 8 characters and it should include numbers, upper, and lower case letters.</small>
                    </div>
                </div>

                <div class="row">
                    <div class="small-12 columns">
                        ${
                            pymf.add_input(
                                "password", 
                                name_="confirm_password", 
                                id_="confirm_password",
                                placeholder="Confirm password",
                                required=True, 
                                pattern="password"
                            )
                        }
                    </div>
                </div>

                <a href="#" id="join-erwin-btn" value="Join Erwin" class="button radius success expand">Join Hevn Online</a>

            </form>

            <h6>By clicking "Join Erwin", you agree to our 
            <a href="/assets/terms.html">terms of service and privacy policy</a>.</h6>

            <div id="loading-gif"></div>

            <div class="row" style="padding-top:18px;">
              <div class="small-12 columns">
                <div class="panel callout" id="forgot" style="display:none;">
                  <h5>There was a problem</h5>
                  <br>
                </div>
              </div>
            </div>

        </div>
    
    </div>
</div>


<div id="messages-reveal" class="reveal-modal medium" data-reveal>
    <h4 class="subheader" id="message-title"></h4>
    <hr>
    <h5 class="subheader" id="message-body"></h5>
    <a class="close-reveal-modal">&#215;</a>
</div>


<script src="/foundation/js/foundation.min.js"></script>
<script src="/foundation/js/foundation/foundation.abide.js"></script>


<script>
    $(document).foundation();
</script>

<script type="text/javascript">

function checkForm(){
  var x = document.forms["signup-form"]["password"].value;
  var xx = document.forms["signup-form"]["confirm_password"].value;
  console.log(x+" "+xx);
  return true;
}

$("#join-erwin-btn").click(function(event){

  event.preventDefault();

  var form = $("#signup-form");
  
  if(checkForm()==false){
    return false;
  }
  var result;

  data = form.serializeArray();
  
  $.ajax({
    type: 'POST',
    url: '/signup',
    data: data,
    success: function(data) {
      result = data.results[0]
      return window.location.href = "/login";
    },
    error: function(jqXHR, textStatus, errorThrown){
      if(jqXHR.status==409){
          $("#message-title").html("Error");
          $("#message-body").html("This account already exists. Please log in normally.");
          $("#messages-reveal").foundation('reveal', 'open');
      }else if(jqXHR.status==422){
          $("#message-title").html("Error");
          $("#message-body").html(jqXHR.responseText);
          $("#messages-reveal").foundation('reveal', 'open');
      }else{
          $("#forgot").show("fast");
      }
    },
    complete: function(){
      $("#loading-gif").html("");
    }
  });
});


</script>


</body>

<%namespace name="pymf" file="modelfuncs.mako"/>

</html>
