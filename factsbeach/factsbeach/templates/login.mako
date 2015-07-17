<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width"/>
<title>Facts Beach :: Login</title>

<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href='/css/materialize/css/materialize.min.css' rel='stylesheet' type='text/css'>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<script type="text/javascript" src="/css/materialize/js/materialize.min.js"></script>


<style type="text/css">
    
    
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


<div class="container">

    <p>&nbsp</p>

    %if logged_in != None:
    <div class="row">
        <h5>You are logged in</h5>
    </div>
    %else:

    <div class="row">
        <h3>Welcome</h3>
    </div>

    <div class="row">
        <div class="col s12 m8">
        <form id="signin-form" method="POST" action="/login">

            <div class="input-field col s12">
                ${
                    pymf.add_input(
                        "text", 
                        name_="login", 
                        id_="login",
                        required=True
                    )
                }
                <label for="login">Email Address</label>
            </div>

            <div class="input-field col s12">
                ${
                    pymf.add_input(
                        "password", 
                        name_="password", 
                        id_="password",
                        required=True
                    )
                }
                <label for="login">Password</label>
            </div>

            <p>&nbsp</p>

            <div class="input-field col s12">

                <input type="hidden" name="form.submitted" value="true" />
                <input type="hidden" name="resp" value="html"/>
                <input type="hidden" name="app_name" value="Hevn Online" />
                <input type="hidden" name="device_token" value="BROWSER_DEVICE_TOKEN" />

                <button class="btn waves-effect waves-light" id="login-btn" type="submit" name="form.submitted" 
                    value="Login">Login
                </button>

            </div>

        </form>
        </div>
    </div>
    %endif



</div>



</body>


</html>


<%namespace name="pymf" file="modelfuncs.mako"/>

