<!doctype html>

<html>
<head>

<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width"/>

<link rel="icon" 
      type="image/png" 
      href="" />

<title>Facts Beach</title>

<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href='/css/materialize/css/materialize.min.css' rel='stylesheet' type='text/css'>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<script type="text/javascript" src="/css/materialize/js/materialize.min.js"></script>


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
        %else:
        <li><a href="/signup">Signup</a></li>
        <li><a href="/login">Login</a></li>
        %endif
      </ul>
    </div>
</nav>

<p>&nbsp</p>


<div class="container">
  <h3>Welcome!</h3>
  <p>A gameplay analytics engine from <a href="http://migacollabs.com">Miga</a></p>
  <p>Free to use, open-source, simple and straight-forward</p>
  <p><a href="http://github.com/migacollabs/factsbeach">On Github</a></p>
  <p>Enjoy!</p>
</div>


</body>


</html>

<%namespace name="pymf" file="modelfuncs.mako"/>